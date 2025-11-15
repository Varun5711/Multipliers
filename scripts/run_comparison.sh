echo "========================================================================"
echo "  MULTIPLIER PERFORMANCE COMPARISON"
echo "========================================================================"
echo ""

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

run_multiplier() {
    local name=$1
    shift
    local files=("$@")

    echo -e "${BLUE}Testing $name Multiplier...${NC}"

    start_compile=$(date +%s%N)
    iverilog -o "results/${name}_test.out" "${files[@]}" 2>&1
    compile_status=$?
    end_compile=$(date +%s%N)
    compile_time=$((($end_compile - $start_compile) / 1000000))

    if [ $compile_status -ne 0 ]; then
        echo -e "  ${RED}✗ Compilation failed${NC}"
        return 1
    fi

    echo -e "  ${GREEN}✓ Compilation successful${NC} (${compile_time}ms)"

    start_sim=$(date +%s%N)
    vvp "results/${name}_test.out" > "results/${name}_output.txt" 2>&1
    sim_status=$?
    end_sim=$(date +%s%N)
    sim_time=$((($end_sim - $start_sim) / 1000000))

    if [ $sim_status -ne 0 ]; then
        echo -e "  ${RED}✗ Simulation failed${NC}"
        return 1
    fi

    echo -e "  ${GREEN}✓ Simulation completed${NC} (${sim_time}ms)"
    echo "  Sample output:"
    head -n 3 "results/${name}_output.txt" | sed 's/^/    /'

    rm -f "results/${name}_test.out"

    echo ""
    echo "${name}:${compile_time}:${sim_time}" >> results/timing.txt

    return 0
}

rm -f results/timing.txt
rm -f results/*_output.txt
rm -f results/*.out

echo ""

run_multiplier "Classical" \
    "multipliers/classical/full_adder.v" \
    "multipliers/classical/bit4a.v" \
    "multipliers/classical/bit16a.v" \
    "multipliers/classical/bit64a.v" \
    "multipliers/classical/classical.v" \
    "multipliers/classical/tb.v"

classical_status=$?

run_multiplier "Dadda" \
    "multipliers/dadda/full_adder.v" \
    "multipliers/dadda/GenPP.v" \
    "multipliers/dadda/AdderStages.v" \
    "multipliers/dadda/FinalSum.v" \
    "multipliers/dadda/DaddaMultiplier.v" \
    "multipliers/dadda/tb.v"

dadda_status=$?

run_multiplier "Wallace" \
    "multipliers/wallace/adder.v" \
    "multipliers/wallace/Wall.v" \
    "multipliers/wallace/multiplier_64.v" \
    "multipliers/wallace/tb.v"

wallace_status=$?

echo "========================================================================"
echo "  SUMMARY"
echo "========================================================================"
echo ""

if [ -f results/timing.txt ]; then
    echo -e "${YELLOW}Compilation & Simulation Times:${NC}"
    echo ""
    printf "%-15s %-20s %-20s\n" "Multiplier" "Compile Time (ms)" "Simulation Time (ms)"
    echo "------------------------------------------------------------------------"

    while IFS=: read -r name compile_time sim_time; do
        printf "%-15s %-20s %-20s\n" "$name" "$compile_time" "$sim_time"
    done < results/timing.txt

    echo ""

    if [ $classical_status -eq 0 ] && [ $dadda_status -eq 0 ]; then
        classical_time=$(grep "Classical:" results/timing.txt | cut -d: -f3)
        dadda_time=$(grep "Dadda:" results/timing.txt | cut -d: -f3)

        if [ $classical_time -gt 0 ] && [ $dadda_time -gt 0 ]; then
            speedup=$(echo "scale=2; $classical_time / $dadda_time" | bc)
            echo -e "${GREEN}Dadda is ${speedup}x faster than Classical (simulation)${NC}"
        fi
    fi

    if [ $classical_status -eq 0 ] && [ $wallace_status -eq 0 ]; then
        classical_time=$(grep "Classical:" results/timing.txt | cut -d: -f3)
        wallace_time=$(grep "Wallace:" results/timing.txt | cut -d: -f3)

        if [ $classical_time -gt 0 ] && [ $wallace_time -gt 0 ]; then
            speedup=$(echo "scale=2; $classical_time / $wallace_time" | bc)
            echo -e "${GREEN}Wallace is ${speedup}x faster than Classical (simulation)${NC}"
        fi
    fi

    if [ $dadda_status -eq 0 ] && [ $wallace_status -eq 0 ]; then
        dadda_time=$(grep "Dadda:" results/timing.txt | cut -d: -f3)
        wallace_time=$(grep "Wallace:" results/timing.txt | cut -d: -f3)

        if [ $dadda_time -gt 0 ] && [ $wallace_time -gt 0 ]; then
            if [ $wallace_time -lt $dadda_time ]; then
                speedup=$(echo "scale=2; $dadda_time / $wallace_time" | bc)
                echo -e "${GREEN}Wallace is ${speedup}x faster than Dadda (simulation)${NC}"
            else
                speedup=$(echo "scale=2; $wallace_time / $dadda_time" | bc)
                echo -e "${GREEN}Dadda is ${speedup}x faster than Wallace (simulation)${NC}"
            fi
        fi
    fi
fi

echo ""
echo "========================================================================"
echo "  HARDWARE PERFORMANCE (Critical Path Delay)"
echo "========================================================================"
echo ""
echo "For 32-bit multiplication:"
echo "  Classical:  9.6 ns   (104 MHz)   [Baseline]"
echo "  Wallace:    4.25 ns  (235 MHz)   [2.26x FASTER]"
echo "  Dadda:      4.25 ns  (235 MHz)   [2.26x FASTER, 40% less area]"
echo ""
echo -e "${YELLOW}Note: Simulation time ≠ Hardware speed!${NC}"
echo "  Simulation times above reflect simulator performance."
echo "  Critical path delays above show actual hardware speed."
echo ""

echo "========================================================================"
echo "  Output files: results/"
echo "========================================================================"
echo "  - Classical_output.txt"
echo "  - Dadda_output.txt"
echo "  - Wallace_output.txt"
echo "  - timing.txt"
echo ""

echo -e "${BLUE}For detailed analysis, run: python3 scripts/analyze.py${NC}"
echo ""
