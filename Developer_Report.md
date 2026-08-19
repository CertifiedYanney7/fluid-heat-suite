# Developer Report: Fluid Flow & Heat Transfer Suite

### 1. Engineering Insight Revealed by the Application
Testing Module A (Pipe Flow Analyser) demonstrates the non-linear pressure drop penalty that occurs during the transition from laminar to turbulent flow. For a 50 mm diameter pipe, increasing flow rate past the critical Reynolds threshold ($Re \approx 2000$) causes friction loss to scale proportionally with $v^2$ rather than linearly with $v$. This visually highlights why pipeline engineers design system operating points to stay within optimal flow regimes to minimize pumping power costs.

### 2. Technical Challenge Overcome
A key challenge was preventing runtime math domain crashes in Module B (Newton's Law of Cooling). Calculating time to reach a target temperature requires a natural logarithm:
$$t = -\frac{1}{k_c} \ln\left(\frac{T_{\text{target}} - T_\infty}{T_0 - T_\infty}\right)$$
If $T_{\text{target}}$ falls outside the range between $T_0$ and $T_\infty$, the argument becomes negative or zero, causing Python to crash. This was resolved by dynamically setting Streamlit slider boundaries so $T_{\text{target}}$ remains strictly bounded between initial and ambient temperatures.

### 3. Future Enhancements
With more development time, I would expand Module A to include multiphase oil-water flow pressure drop correlations (e.g., Beggs and Brill) and extend Module B to analyze multi-layer composite wall conduction.