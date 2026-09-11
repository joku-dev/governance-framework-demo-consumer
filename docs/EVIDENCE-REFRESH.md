# Refresh governance evidence

The 11 September 2026 maintenance review requested current DevSecOps,
architecture and typed vulnerability evidence from this demo consumer.

1. Merge the reviewed maintenance change. The resulting push to `main` starts
   the existing DevSecOps and architecture workflows against that exact commit.
2. Inspect the actual reports. Both governance domains remain report-only;
   workflow success does not certify that all governance criteria passed.
3. Collect the DevSecOps and architecture results in the central governance
   repository. Also collect `application-evidence` from the DevSecOps run through
   the separate typed-evidence intake.
4. Review run identity, subject digests, Trust findings and context, then merge
   the proposed intake records before presenting the updated central viewer.

Manual workflow runs remain diagnostic history and cannot replace an available
official `main` push result. Historical evidence must not be overwritten or
re-dated. Newly generated reports may reveal open controls even when the
technical workflow completes successfully.

This maintenance refresh retains the existing baseline pins, report-only modes,
application behavior and branch review requirement. It does not approve new
blocking gates or assert the result of a run that has not completed.
