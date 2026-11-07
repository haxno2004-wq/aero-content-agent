---
layout: post
title: "Hourglassing in Explicit FEA: Spotting and Controlling Zero-Energy Modes"
description: "Practical guide identifying hourglass modes in explicit FEA, explaining why they occur in reduced integration elements, how to detect them in results, and proven methods to suppress or prevent them in LS-DYNA, ANSYS, and Abaqus."
tags: ["cfd", "ansys", "ls-dyna", "abaqus", "explicit-fem", "fem", "structural-analysis"]
hero: assets/covers/hourglassing-in-explicit-fea-spotting-and-controlling-zero-e.svg
date: 2026-11-07 09:00:00 +0530
---

<h2>Introduction to Spurious Zero-Energy Modes</h2>
<p>In explicit finite element analysis (FEA), particularly when using reduced-integration elements, analysts often encounter a phenomenon known as hourglassing. This is a spurious deformation mode that consumes zero strain energy, allowing the element to deform without resisting forces. While the solver may not flag this as an immediate error, unchecked hourglassing can lead to non-physical results, mesh instability, and failure to capture genuine structural behavior. Understanding how to spot and control these zero-energy modes is essential for anyone performing crash simulation, penetration analysis, or high-velocity impact studies using explicit dynamics.</p>

<h2>Why Hourglassing Occurs in Reduced-Integration Elements</h2>
<p>Hourglassing is inherently tied to the integration scheme employed within an element. Standard full-integration elements compute strain at multiple Gauss points, providing a stiff but often overly restrictive model. Reduced-integration elements use fewer Gauss points—typically one integration point per element—to reduce computational cost and avoid shear locking in nearly incompressible materials. However, this reduction creates a gap: the strain-displacement matrix no longer has full rank, leaving certain nodal displacement patterns that produce zero strain energy. These patterns are the hourglass modes.</p>

<p>The physical interpretation is that the element can "shear" in a specific pattern resembling an hourglass shape, where opposite corners move in opposite directions while the center remains relatively stationary. Because the reduced integration scheme cannot distinguish this deformation from a zero-strain state, the element offers no resistance. In a dynamic simulation, this can manifest as a sudden, non-physical acceleration of the structure, effectively lowering the system's apparent stiffness.</p>

<h2>Identifying Hourglassing in Post-Processing</h2>
<p>Detecting hourglassing requires a careful look at the deformation shape and the energy balance of the model. The most direct method is to examine the hourglass energy output provided by the solver. In LS-DYNA, for example, the output variable <code>HOURGLASS ENERGY</code> or the <code>HGENER</code> result output variable quantifies the energy associated with these spurious modes. A rising hourglass energy relative to the total internal energy is a red flag.</p>

<p>Beyond the energy plot, visual inspection of the deformed shape is critical. Hourglass modes typically exhibit a characteristic pattern: nodal displacements that create a "waisting" effect in shell elements or a checkerboard-like pattern in solid elements. In shell elements, the hourglass mode often involves the top and bottom surfaces moving in opposite directions while the midsurface remains flat. In solid elements, the deformation may look like alternating bulges and indentations across the element volume.</p>

<p>Another indicator is the convergence of the solution. If the global residual forces do not balance or if the displacement history shows oscillatory behavior without physical justification, hourglassing may be contributing to the numerical instability. It is important to differentiate this from physical plasticity or large deformation effects; hourglassing is a numerical artifact, not a material response.</p>

<h2>Techniques to Suppress and Control Hourglassing</h2>
<p>Once hourglassing is identified, several strategies exist to mitigate or eliminate it. The choice of method depends on the element type, the material model, and the specific goals of the simulation.</p>

<h3>Increased Integration</h3>
<p>The most straightforward approach is to switch from reduced integration to full integration. By increasing the number of Gauss points, the stiffness matrix becomes full rank, and the spurious modes are eliminated. However, this comes with a trade-off. Full integration significantly increases the computational cost because more strain evaluations are required per time step. Additionally, full-integration elements are susceptible to shear locking when modeling thin structures or nearly incompressible materials, which can artificially stiffen the model and prevent realistic deformation.</p>

<h3>Hourglass Control Algorithms</h3>
<p>Modern explicit solvers incorporate hourglass control algorithms designed to add artificial stiffness specifically in the zero-energy modes without restoring the full integration cost. In LS-DYNA, the <code>HG control</code> card or the <code>Hourglass Control</code> command allows the user to select from several algorithms:</p>
<ul>
  <li><strong>Type I (Default):</strong> Adds stiffness based on the hourglass energy, effectively damping the mode. This is the most robust default for general use.</li>
  <li><strong>Type II:</strong> Uses a different formulation that may be preferable for specific material models or element types.</li>
  <li><strong>Type III:</strong> Often used for shell elements to provide more targeted control.</li>
</ul>
<p>These algorithms typically introduce a penalty term into the element stiffness matrix that resists the hourglass displacement pattern. The key is that this stiffness is activated only when the hourglass mode is detected, preserving the computational efficiency of reduced integration while suppressing the spurious deformation.</p>

<h3>Hourglass Viscosity</h3>
<p>Another effective method is the introduction of hourglass viscosity. This technique adds a damping force proportional to the rate of change of the hourglass displacement. Physically, this mimics the effect of material damping or internal friction, smoothing out the numerical oscillations associated with the mode. In LS-DYNA, this is often controlled via the <code>HG VISCOSITY</code> parameter. Hourglass viscosity is particularly useful in crash simulations where some numerical damping is acceptable and even desirable to ensure solution stability.</p>

<h3>Element Selection and Refinement</p>
<p>Sometimes the best remedy is a change in the discretization strategy. Using a different element type that does not suffer from the same integration issues can resolve the problem. For shell structures, switching from a reduced-integration shell to a fully integrated shell or a shell with enhanced strain capabilities may be necessary. For solid models, using reduced-integration hexahedra with hourglass control is standard, but transitioning to eight-node solid elements with full integration in critical regions can provide a more robust solution. Mesh refinement also helps; a finer mesh reduces the size of individual elements, and the relative impact of hourglass modes on the overall system stiffness diminishes.</p>

<h2>Common Pitfalls and Best Practices</h2>
<p>When working with explicit FEA, several common mistakes can either trigger hourglassing or mask its presence. Being aware of these can save significant time during verification.</p>

<p><strong>Mistake 1: Ignoring the Hourglass Energy Output.</strong> Many analysts focus solely on the global residual forces and internal energy, overlooking the hourglass energy component. Always monitor the hourglass energy output throughout the run, not just at the end.</p>

<p><strong>Mistake 2: Over-Reliance on Hourglass Control Without Physical Justification.</strong> While hourglass control is a powerful tool, turning it on without understanding why the mode is occurring can lead to misleading results. The added artificial stiffness may suppress the numerical mode but could also mask a genuine modeling issue, such as insufficient mesh density or incorrect boundary conditions.</p>

<p><strong>Mistake 3: Using Full Integration as a Crutch.</strong> Switching to full integration to "fix" hourglassing is not always appropriate. As noted, shear locking can become the dominant issue, leading to a model that is too stiff to capture the intended physics, such as bending of thin shells or contact deformation.</p>

<p><strong>Best Practice: Verify with a Convergence Study.</strong> If hourglassing is suspected, perform a mesh convergence study. Refine the mesh and observe whether the hourglass energy decreases relative to the total energy. If the problem persists or worsens with refinement, the root cause is likely something other than the integration scheme, such as contact instability or material model nonlinearities.</p>

<h2>Conclusion</h2>
<p>Hourglassing is a quintessential challenge in explicit FEA that arises from the use of reduced-integration elements. It is a zero-energy mode that allows non-physical deformation, potentially compromising the integrity of the simulation results. By understanding the root cause— the rank deficiency of the strain-displacement matrix under reduced integration—analysts can effectively identify the tell-tale signs in post-processing and apply the appropriate controls. Whether through hourglass control algorithms, viscosity settings, or strategic element selection, the goal is to maintain the computational efficiency of reduced integration while ensuring the structural response remains physically realistic. For the practicing engineer, mastering these techniques is not just about avoiding solver warnings; it is about ensuring that the simulation accurately represents the behavior of the actual structure under dynamic loading.</p>