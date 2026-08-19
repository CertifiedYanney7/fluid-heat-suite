import math
import numpy as np


class Fluid:
    """Represents fluid physical properties required for engineering calculations."""

    PRESETS = {
        "Water": {"density": 998.2, "viscosity": 0.001002},
        "Air": {"density": 1.204, "viscosity": 0.00001825},
        "Crude Oil": {"density": 850.0, "viscosity": 0.015000},
    }

    def __init__(
        self,
        name: str = "Water",
        density: float = None,
        viscosity: float = None,
    ):
        self.name = name
        if name in self.PRESETS and density is None and viscosity is None:
            self.density = self.PRESETS[name]["density"]
            self.viscosity = self.PRESETS[name]["viscosity"]
        else:
            if density is None or viscosity is None:
                raise ValueError(
                    "Custom fluids require explicit density and viscosity values."
                )
            self.density = float(density)
            self.viscosity = float(viscosity)

        self._validate()

    def _validate(self):
        if self.density <= 0:
            raise ValueError("Density must be greater than zero.")
        if self.viscosity <= 0:
            raise ValueError("Viscosity must be greater than zero.")


class Pipe:
    """Represents cylindrical pipe geometry and fluid dynamics."""

    def __init__(
        self,
        diameter: float,
        length: float,
        roughness: float = 0.000045,
    ):
        self.diameter = float(diameter)
        self.length = float(length)
        self.roughness = float(roughness)
        self._validate()

    def _validate(self):
        if self.diameter <= 0:
            raise ValueError("Pipe diameter must be greater than zero.")
        if self.length <= 0:
            raise ValueError("Pipe length must be greater than zero.")
        if self.roughness < 0:
            raise ValueError("Pipe roughness cannot be negative.")

    def area(self) -> float:
        """Calculates cross-sectional area (m^2)."""
        return (math.pi * self.diameter**2) / 4.0

    def velocity(self, flow_rate: float) -> float:
        """Calculates average flow velocity (m/s)."""
        if flow_rate < 0:
            raise ValueError("Flow rate cannot be negative.")
        return flow_rate / self.area()

    def reynolds_number(self, fluid: Fluid, flow_rate: float) -> float:
        """Calculates dimensionless Reynolds Number (Re)."""
        v = self.velocity(flow_rate)
        return (fluid.density * v * self.diameter) / fluid.viscosity

    def friction_factor(self, reynolds: float) -> float:
        """Calculates Darcy friction factor (f). Uses 64/Re for laminar, Swamee-Jain for turbulent."""
        if reynolds <= 0:
            return 0.0
        elif reynolds <= 2000:
            return 64.0 / reynolds
        else:
            rel_roughness = self.roughness / self.diameter
            term = (rel_roughness / 3.7) + (5.74 / (reynolds**0.9))
            return 0.25 / (math.log10(term) ** 2)

    def pressure_drop(self, fluid: Fluid, flow_rate: float) -> dict:
        """Calculates pressure drop using Darcy-Weisbach equation."""
        if flow_rate == 0:
            return {
                "velocity": 0.0,
                "reynolds": 0.0,
                "flow_regime": "Static",
                "friction_factor": 0.0,
                "delta_p_pa": 0.0,
                "delta_p_bar": 0.0,
            }

        v = self.velocity(flow_rate)
        re = self.reynolds_number(fluid, flow_rate)
        f = self.friction_factor(re)
        delta_p_pa = f * (self.length / self.diameter) * (
            fluid.density * (v**2) / 2.0
        )

        regime = (
            "Laminar"
            if re <= 2000
            else ("Transitional" if re <= 4000 else "Turbulent")
        )

        return {
            "velocity": v,
            "reynolds": re,
            "flow_regime": regime,
            "friction_factor": f,
            "delta_p_pa": delta_p_pa,
            "delta_p_bar": delta_p_pa / 100000.0,
        }


class HeatTransfer:
    """Performs conduction and transient cooling calculations."""

    @staticmethod
    def conduction_flat_wall(
        k: float, area: float, thickness: float, t_inside: float, t_outside: float
    ) -> float:
        """Calculates steady-state conduction heat rate (W) via Fourier's Law."""
        if k <= 0 or area <= 0 or thickness <= 0:
            raise ValueError(
                "Thermal conductivity, area, and thickness must be strictly positive."
            )
        return (k * area * (t_inside - t_outside)) / thickness

    @staticmethod
    def newton_cooling_temperature(
        time: float, t0: float, t_inf: float, k_c: float
    ) -> float:
        """Calculates temperature at time t during Newton cooling."""
        if time < 0 or k_c <= 0:
            raise ValueError("Time must be non-negative and k_c must be positive.")
        return t_inf + (t0 - t_inf) * math.exp(-k_c * time)

    @staticmethod
    def time_to_target_temp(
        t0: float, t_target: float, t_inf: float, k_c: float
    ) -> float:
        """Calculates time required to reach a target temperature."""
        if k_c <= 0:
            raise ValueError("Cooling rate constant must be positive.")

        if t0 > t_inf and not (t_inf < t_target < t0):
            raise ValueError(
                f"Target temp ({t_target}°C) must be between initial ({t0}°C) and ambient ({t_inf}°C)."
            )
        if t0 < t_inf and not (t0 < t_target < t_inf):
            raise ValueError(
                f"Target temp ({t_target}°C) must be between initial ({t0}°C) and ambient ({t_inf}°C)."
            )

        ratio = (t_target - t_inf) / (t0 - t_inf)
        return -1.0 / k_c * math.log(ratio)