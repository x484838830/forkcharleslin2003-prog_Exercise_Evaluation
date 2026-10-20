# rwg — within-group agreement index (James, Demaree and Wolf 1984)

> Source: https://search.r-project.org/CRAN/refmans/multilevel/html/rwg.html and https://search.r-project.org/CRAN/refmans/multilevel/html/rwg.j.html (R package multilevel, author Paul Bliese)
> Collected: 2026-10-20
> Published: Unknown

Kind of file: reading notes with the formulas and short verbatim quotes. It is not the full text.

## Notes

- Original paper: James, L.R., Demaree, R.G., & Wolf, G. (1984). Estimating within-group interrater reliability with and without response bias. Journal of Applied Psychology, 69, 85-98.
- Single-item formula, as the documentation writes it: rwg = 1-(Observed Group Variance/Expected Random Variance)
- James et al. (1984) recommend truncation when the observed group variance is larger than the expected random variance. The truncation gives rwg = 0, which means no agreement.
- The default expected random variance is 2. The value of 2 is the variance of a rectangular distribution when there are 5 response options.
- For another number of response options, the rectangular variance is ranvar=(A^2-1)/12, where A is the number of response options.
- The documentation adds that the rectangular distribution is widely used, but other random values may be more appropriate.
- rwg.j is the version for scales with several items.
