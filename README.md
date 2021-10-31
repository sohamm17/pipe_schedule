##Artifact of "End-to-end Scheduling of Real-time Task Pipelines on Multiprocessors"

### Constraint Solvers

1. Our heuristic constraint solver algorithm: `CoPi`
2. `GEKKO`: The APOPT Solver: https://machinelearning.byu.edu/

Most experiments compare the above two. We also compared two other
MINLP solvers but only for the first experiment:

1. `pyomo`: http://www.pyomo.org/
2. `scipy`: https://docs.scipy.org/doc/scipy/reference/optimize.html

### Requirements

Please follow the installation procedure of `GEKKO`, `pyomo`, `scipy`, `pickle` (for reading and writing dataset). We believe that the code should work for python version 3.5 and 3.6. We have run all the experiments with python 3.6. If not sure, please use [`virtualenv`](https://virtualenv.pypa.io/en/latest/) to install python 3.6 .

### Algorithms and Files
The CoPi algorithms are at the root location of the source directory.
The MINLP solver implementations are in `ilp/`.

CoPi files are:
1. `copi_e2e.py`: For only E2E Delay Constraint implementation.
2. `copi_all.py`: For all the constraints.
3. `multi_pipeline.py`: For the multiprocessor experiments with CoPi.

MINLP Solvers:
1. `ilp/ilp_gekko.py`: `GEKKO` constraint optimization solution.
2. `ilp/ilp_pyomo.py`: `pyomo` constraint optimization solution.
3. `ilp/ilp_scipy.py`: `scipy` constraint optimization solution.

Helper function files:
1. `utility.py`: Some helper functions for utilization, RMS bound and other calculations.
2. `pipeline.py`: Most functions related to a pipeline are here. For example, end-to-end delay, loss-rate, etc.

## Experiments

The next subsections correspond to the subsections in the Evaluation section of the paper.

### Uniprocessor Acceptance Ratio Experiments

#### Only for End-to-end Constraint

#### Both End-to-end and Loss-rate Constraints

### Solver Runtime Overhead

### Performance Insight of CoPi

### Multiprocessor Experiments
