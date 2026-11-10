---
layout: post
title: "Failure Criteria for Composite Laminates: Tsai-Wu, Hashin and Puck Compared"
description: "A practical comparison of the three most widely used failure criteria for composite laminates—Tsai-Wu, Hashin, and Puck—covering their theoretical basis, implementation in ANSYS, and guidance on when to use each."
tags: ["cfd", "ansys", "composites", "hashin", "puck", "tsai-wu", "fem", "structural-analysis"]
hero: assets/covers/failure-criteria-for-composite-laminates-tsai-wu-hashin-and.svg
date: 2026-11-10 09:00:00 +0530
---

<h2>Introduction</h2>
<p>Composite materials are prized in aerospace, automotive, and renewable energy applications for their high strength-to-weight ratios and design flexibility. However, predicting when and how a composite laminate will fail under complex loading remains one of the most critical—and challenging—tasks in structural analysis. Unlike isotropic materials, which fail by a single yield criterion, composites exhibit direction-dependent stiffness and strength, and failure can initiate through multiple mechanisms: matrix cracking, fiber breaking, delamination, and interfacial debonding.</p>
<p>Engineers rely on failure criteria to translate the complex stress state at any point in a laminate into a single non-dimensional parameter, often called the <strong>failure index</strong>. When this index exceeds unity, the material is predicted to have failed according that specific model. This article provides a detailed comparison of the three most widely used criteria—<strong>Tsai-Wu</strong>, <strong>Hashin</strong>, and <strong>Puck</strong>—from their theoretical foundations to practical implementation considerations in ANSYS (Fluent/CFX coupling or Mechanical). By the end, you will have a clear understanding of the strengths and limitations of each method and how to select the right one for your simulation workflow.</p>

<h2>The Tsai-Wu Failure Criterion</h2>
<h3>Theory and Tensor Polynomial Form</h3>
<p>The <strong>Tsai-Wu criterion</strong> is an interactive quadratic failure criterion that was among the first to account for the interaction between normal and shear stresses. It is expressed as a tensor polynomial in the stress components:</p>
<ul>
<li><strong>Quadratic form:</strong> <em>F</em><sub>i</sub><em>σ</em><sub>i</sub> + <em>F</em><sub>ij</sub><em>σ</em><sub>i</sub><em>σ</em><sub>j</sub> = 1</em>, where the double-sum runs over the in-plane stress components.</li>
<li><strong>Linear terms</strong> (<em>F</em><sub>i</sub>) capture the individual effects of normal stresses in the 1, 2, and 3 directions (fiber, transverse, and through-thickness).</li>
<li><strong>Quadratic interaction terms</strong> (<em>F</em><sub>ij</sub>) capture the coupling between different stress components, such as <em>σ</em><sub>1</sub><em>σ</em><sub>2</sub>.</li>
</ul>
<p>Because the Tsai-Wu criterion is expressed in terms of the stress tensor only, it does not distinguish between tension and compression in the fiber direction beyond their respective linear coefficients. It is essentially an extension of the maximum-stress concept, enriched with interaction terms that improve accuracy under biaxial stress states.</p>

<h3>Practical Implementation</h3>
<p>In practice, the coefficients <em>F</em><sub>i</sub> and <em>F</em><sub>ij</sub> are derived from unidirectional coupon test data: tensile and compressive strengths in the fiber and transverse directions, and shear strength on the major material planes. Once these material properties are identified, the criterion can be evaluated at every integration point of the finite element mesh.</p>
<p><strong>Strengths:</strong> Requires relatively few material parameters; computationally inexpensive; works well for quasi-isotropic laminates under moderate biaxial loading.</p>
<p><strong>Limitations:</strong> It is an empirical fit and does not have a strong physical basis for predicting the <em>mode</em> of failure (e.g., whether matrix cracking or fiber breaking occurs first). It also tends to be conservative in pure shear and may over-predict failure under certain multiaxial stress states.</p>

<h2>The Hashin Failure Criterion</h2>
<h3>Theory and Mode-Specific Decomposition</h3>
<p><strong>Hashin’s criterion</strong>, introduced in the 1980s, takes a fundamentally different approach. Instead of a single polynomial, it defines separate failure indices for each constituent of the composite: the fiber, the matrix, and the fiber-matrix interface. This mode-specific decomposition is its greatest advantage.</p>
<ul>
<li><strong>Fiber tension failure:</strong> Failure is predicted when the axial stress in the fiber exceeds its tensile strength.</li>
<li><strong>Fiber compression failure:</strong> A distinct check for compressive buckling or micro-buckling of the fiber.</li>
<li><strong>Matrix tension failure:</strong> Failure occurs when the transverse stress exceeds the matrix tensile strength, often accompanied by a shear term.</li>
<li><strong>Matrix compression failure:</strong> Predicts transverse cracking or kinking under compressive loading.</li>
</ul>
<p>Each of these four mechanisms has its own algebraic expression, typically involving the stresses projected onto the fiber and transverse directions, as well as the relevant strength parameters.</p>

<h3>Practical Implementation</h3>
<p>To use Hashin’s criterion, you need the unidirectional tensile and compressive strengths for both fiber and matrix, as well as the in-plane and out-of-plane shear strengths. In ANSYS Mechanical, the Hashin option is available under the Failure Criterion settings for composite materials. The solver evaluates all four indices at each integration point and the laminate is considered failed if <strong>any</strong> single index exceeds unity.</p>
<p><strong>Strengths:</strong> Physically intuitive; predicts the <em>type</em> of failure (fiber break vs. matrix crack vs. interface debond); widely validated against experimental data across a range of loading conditions.</p>
<p><strong>Limitations:</strong> Requires more material property inputs than Tsai-Wu; the separate indices can sometimes predict concurrent failure modes that are physically overlapping, requiring post-processing judgment; less effective for highly angle-ply laminates where stress redistribution is complex.</p>

<h2>The Puck Failure Criterion</h2>
<h3>Theory and Micro-Mechanical Foundations</h3>
<p><strong>Puck’s criterion</strong>, developed in the 1990s, is often regarded as the most comprehensive of the three for predicting composite laminate failure. Like Hashin, it is mode-specific, but it is built on a more detailed micro-mechanical framework that distinguishes between different failure planes within the representative volume element (RVE).</p>
<ul>
<li><strong>Failure in the fiber direction:</strong> Puck distinguishes between failure on the fiber cross-section and failure on the fiber/matrix interface, each with its own stress-based check.</li>
<li><strong>Failure in the transverse plane:</strong> The criterion evaluates stresses on three distinct planes: the longitudinal-transverse plane, the transverse plane, and the out-of-plane shear plane. This allows it to capture delamination-prone states and transverse cracking more reliably.</li>
<li><strong>Interaction terms:</strong> Puck includes explicit interaction terms between normal and shear stresses on these planes, which improves accuracy under complex, non-proportional loading paths.</li>
</ul>
<p>The mathematical expressions are more involved than Tsai-Wu, but they are grounded in the physics of fiber breakage, matrix cracking, and interface debonding as predicted by micromechanics models.</p>

<h3>Practical Implementation</h3>
<p>Implementing Puck’s criterion in ANSYS requires defining the full set of Puck-specific material parameters: fiber tensile and compressive strengths, matrix tensile and compressive strengths, and a set of shear strengths on the three defined planes. Additionally, Puck’s model includes parameters related to the fiber radius and matrix properties that affect the stress distribution around the fiber.</p>
<p>In the ANSYS Mechanical interface, selecting “Puck” under the Failure Criterion menu will prompt you to input these parameters. The solver then computes the failure indices for each of the relevant planes and reports the maximum index. A value greater than 1 indicates failure according to the Puck model.</p>
<p><strong>Strengths:</strong> Most physically grounded of the three; excellent at predicting delamination and transverse cracking; handles angle-ply and cross-ply laminates with high fidelity; provides insight into which specific plane is driving the failure.</p>
<p><strong>Limitations:</strong> Highest number of required material inputs; more computationally expensive due to the plane-by-plane evaluation; implementation can be less straightforward if your material database is calibrated only for Tsai-Wu or Hashin.</p>

<h2>Comparative Summary and Decision Guidance</h2>
<table style="width:100%; border-collapse:collapse; margin: 1.5em 0;">
<thead>
<tr style="background:#f5f5f5;"><th style="padding:0.5em; border:1px solid #ccc;">Criterion</th><th style="padding:0.5em; border:1px solid #ccc;">Primary Focus</th><th style="padding:0.5em; border:1px solid #ccc;">Input Requirements</th><th style="padding:0.5em; border:1px solid #ccc;">Best Use Case</th></tr>
</thead>
<tbody>
<tr><td style="padding:0.5em; border:1px solid #ccc;">Tsai-Wu</td><td style="padding:0.5em; border:1px solid #ccc;">Interactive quadratic stress polynomial</td><td style="padding:0.5em; border:1px solid #ccc;">Unidirectional tensile/compressive and shear strengths</td><td style="padding:0.5em; border:1px solid #ccc;">Quick screenings, quasi-isotropic laminates, early-stage design</td></tr>
<tr><td style="padding:0.5em; border:1px solid #ccc;">Hashin</td><td style="padding:0.5em; border:1px solid #ccc;">Mode-specific fiber/matrix/interface checks</td><td style="padding:0.5em; border:1px solid #ccc;">Fiber and matrix tensile/compressive + in-plane/out-of-plane shear strengths</td><td style="padding:0.5em; border:1px solid #ccc;">Laminates where identifying the failure mode (fiber break vs. matrix crack) is critical</td></tr>
<tr><td style="padding:0.5em; border:1px solid #ccc;">Puck</td><td style="padding:0.5em; border:1pm solid #ccc;">Plane-specific micro-mechanical failure analysis</td><td style="padding:0.5em; border:1px solid #ccc;">All Hashin inputs plus fiber radius, matrix properties, and plane-specific shear strengths</td><td style="padding:0.5em; border:1px solid #ccc;">Complex laminates (angle-ply, cross-ply), delamination assessment, final validation runs</td></tr>
</tbody>
</table>

<h2>Common Pitfalls and Best Practices</h2>
<h3>Material Property Calibration</h3>
<p>Regardless of which criterion you choose, the accuracy of your failure prediction hinges on the quality of the input material strengths. A common mistake is using generic or generic “textbook” values without calibrating them to your specific laminate system (fiber type, matrix resin, fiber volume fraction). Always perform at least quasi-static coupon tests—tension, compression, and shear—to extract the true strength values for your composite system.</p>
<h3>Stress State Check</h3>
<p>Failure criteria are only as good as the stress field they are applied to. Ensure that your CFD-CFD or structural analysis mesh is sufficiently refined, especially near geometric discontinuities (holes, cutouts, joint lines) where stress gradients are steep. A coarse mesh can artificially suppress or amplify the failure index, leading to non-conservative or overly conservative results.</p>
<h3>Layup Symmetry and Coupling</p>
<p>For laminates with asymmetric layups, bending-extension coupling induces twist and complex stress distributions. Make sure your composite layup definition in ANSYS accurately reflects the stacking sequence and ply orientations. An incorrect ply angle by just a few degrees can shift the failure index by a significant margin under off-axis loading.</p>
<h3>Post-Processing the Failure Index</h3>
<p>When the failure index exceeds 1, the default ANSYS output tells you “failed,” but it does not tell you <em>why</em>. Post-process the results by exporting the per-index values (Tsai-Wu index, Hashin fiber tension, Hashin matrix compression, Puck longitudinal plane, etc.). This allows you to identify the dominant failure mode and make informed design decisions, such as adding reinforcement, changing ply orientation, or increasing ply thickness.</p>

<h2>Conclusion</h2>
<p>Choosing a failure criterion for composite laminate analysis is a balance between fidelity, computational cost, and the specific failure modes you need to anticipate. The <strong>Tsai-Wu</strong> criterion remains a solid workhorse for rapid assessments and quasi-isotropic structures, requiring minimal input and offering a quick pass/fail check. The <strong>Hashin</strong> criterion provides a meaningful middle ground, decomposing failure into physically distinct modes without the extensive input set required by more advanced models. For complex laminate architectures, angle-ply layups, or when delamination and transverse cracking are primary concerns, the <