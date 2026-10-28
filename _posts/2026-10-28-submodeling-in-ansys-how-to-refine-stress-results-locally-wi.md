---
layout: post
title: "Submodeling in ANSYS: How to Refine Stress Results Locally Without Remeshing Everything"
description: "Learn the step-by-step submodeling workflow in ANSYS to extract high-fidelity stress results in small regions without rebuilding the entire model mesh."
tags: ["ansys", "fluent", "cfx", "static-structural", "submodeling", "meshing", "stress-analysis"]
hero: assets/covers/submodeling-in-ansys-how-to-refine-stress-results-locally-wi.svg
date: 2026-10-28 09:00:00 +0530
---

<h2>Introduction to Submodeling</h2>
<p>In structural simulation, engineers often face a common dilemma: you need accurate stress results in a small, critical region of a model, but generating a globally fine mesh for the entire domain is computationally expensive or impractical. Submodeling (also known as localized mesh refinement or adaptive mesh refinement) is the ANSYS workflow that solves this problem. It allows you to start with a coarse, efficient global mesh, then "submodel" a localized area with a much finer mesh without remeshing the entire model. The result is high‑fidelity stress values exactly where you need them, coupled with the efficiency of a coarse global mesh.</p>

<h2>When to Use Submodeling</h2>
<p>Submodeling is ideal for situations where stress concentrations occur in small features—such as a hole, fillet, weld toe, or joint interface—while the surrounding structure remains relatively uniform. Typical applications include:</p>
<ul>
<li><strong>Hole‑bearing joints</strong> where the stress field around the hole is of interest.</li>
<li><strong>Additive‑manufactured parts</strong> with localized support structures.</li>
<li><strong>Composite laminates</strong> with delamination or matrix‑cracking zones.</li>
<li><strong>Crash‑box or impact‑absorbing structures</strong> with localized deformation.</li>
</ul>
<p>If your design study involves global deformation trends but you also need peak stress values for fatigue or failure assessment, submodeling gives you the best of both worlds.</p>

<h2>The Core Concept: Two‑Mesh Coupling</h2>
<p>The fundamental idea behind submodeling is a two‑mesh coupling process. First, you solve a global analysis with a coarse mesh. The global solution provides "boundary conditions" for a second, local analysis. The local mesh is independent and much finer, but it must be compatible with the displacements and forces computed on the global model’s boundary. ANSYS handles the data transfer automatically, ensuring equilibrium and compatibility across the interface between the coarse and fine meshes.</p>

<h2>Step‑by‑Step Submodeling Workflow in ANSYS Mechanical</h2>
<p>Below is the typical workflow for performing a submodeling analysis in ANSYS Mechanical. The steps are written for the Workbench environment, but the core concepts apply to the native GUI as well.</p>

<h3>1. Define the Global Model</h3>
<p>Start by building your complete structural model. Assign material properties, loads, and boundary conditions. Crucially, apply a mesh that is coarse enough to keep the total node count manageable, but still capable of capturing the overall deformation pattern. Avoid using a mesh that is too coarse in non‑critical regions, as the submodeling results depend on the accuracy of the global displacement field.</p>

<h3>2. Run the Global Analysis</h3>
<p>Solve the global model. This step computes the nodal displacements and reaction forces across the entire model. The solver uses the coarse mesh to obtain a quick, approximate solution. Verify that the global solution has converged and that the deformation pattern makes physical sense before proceeding.</p>

<h3>3. Extract Boundary Data for the Submodel</h3>
<p>Once the global analysis is complete, you need to define the region where the fine mesh will be applied. In ANSYS, this is done using the <strong>Submodeling</strong> tool (typically found under the <strong>Solution</strong> > <strong>Submodeling</strong> menu or via the toolbar). You will select the boundary nodes or faces that enclose the region of interest. ANSYS will extract the nodal displacements from the global solution and use them as essential boundary conditions for the submodel.</p>

<h3>4. Create the Local (Sub) Mesh</h3>
<p>With the boundary conditions extracted, generate a new mesh exclusively for the subregion. This mesh can be dramatically finer than the global mesh—often 5–10 times the element size in critical directions. You can use tetrahedral, hexahedral, or polyhedral elements depending on the geometry and physics. Because the submodel is independent, you have full control over element type, refinement level, and mesh quality metrics.</p>

<h3>5. Apply Boundary Conditions from the Global Step</h3>
<p>ANSYS automatically applies the extracted displacements as <strong>displacement boundary conditions</strong> on the submodel’s boundary. In some cases, you may also need to apply equivalent nodal forces if the global model included distributed loads or body forces that act on the subregion. The software ensures that the fine‑mesh solution is consistent with the coarse‑mesh solution, maintaining global equilibrium.</p>

<h3>6. Solve the Submodel</h3>
<p>Run the local analysis. The solver now uses the fine mesh to compute detailed stress/strain fields within the subregion. Because the boundary displacements are fixed from the global step, the local solver does not need to recompute the entire structure’s response—it only solves for the refined region, which is computationally cheap compared to a full fine‑mesh analysis.</p>

<h3>7. Post‑Process the Results</h3>
<p>After the submodel solve completes, you can plot stress contours, extract peak values, and perform fatigue or failure criteria assessments. The results are directly comparable to those from a full fine‑mesh analysis, but at a fraction of the computational cost. You can also compare the submodel stresses with the global stresses to quantify the stress concentration factor.</p>

<h2>Best Practices and Common Pitfalls</h2>
<p>To get accurate submodeling results, keep the following guidelines in mind:</p>

<ul>
<li><strong>Mesh Independence of the Global Step:</strong> The global mesh must be fine enough to capture the overall stiffness and deformation shape. If the global mesh is too coarse, the extracted boundary displacements will be inaccurate, and the submodel results will be compromised.</li>
<li><strong>Boundary Selection:</strong> Choose boundary nodes that completely surround the region of interest without cutting through features you want to refine. The boundary should ideally follow natural geometry breaks (e.g., a plane through a hole, a cross‑section of a beam).</li>
<li><strong>Equilibrium Check:</strong> After the submodel solve, verify that the internal forces in the subregion are consistent with the extracted boundary tractions. ANSYS typically provides a "force balance" check or you can compare reaction forces.</li>
<li><strong>Avoid Over‑Refinement:</strong> While it is tempting to make the submesh extremely fine, diminishing returns set in once the element size is smaller than the expected plastic zone or fracture process zone. A mesh convergence study on the submodel is still recommended.</li>
<li><strong>Contact and Loads:</strong> If your model includes contact, ensure that the contact status is consistent between the global and local steps. Some load types (e.g., pressure on a curved surface) may need to be re‑applied or scaled appropriately for the submodel.</li>
</ul>

<h2>Verifying Submodeling Results</h2>
<p>A good practice is to run a small “full‑mesh” comparison in the subregion only. Generate a uniformly fine mesh for just that area and solve it independently. Compare the peak stresses and stress distributions between the submodel and the local full‑mesh result. They should agree within a small percentage (typically <5% for well‑posed submodels). If there are large discrepancies, review the boundary selection, global mesh density, and element types.</p>

<h2>Conclusion</h2>
<p>Submodeling is a powerful technique in the ANSYS engineer’s toolkit that bridges the gap between computational efficiency and local accuracy. By leveraging a coarse global mesh and a fine local mesh, you can obtain reliable peak stress values in critical regions without the burden of remeshing the entire model. Follow the workflow outlined above, respect the best‑practice guidelines, and always verify your results against a localized full‑mesh analysis. With experience, submodeling will become a go‑to method for fatigue analysis, failure assessment, and detailed design optimization in your simulation projects.</p>