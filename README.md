# Exercism Python Representer

An [automated anaylsis](analyis) tool that parses a Python file to create a normalized `representation.txt` file per the [representer interface][interface].

It is run with `./bin/run.sh $EXERCISM $PATH_TO_FILES $PATH_FOR_OUTPUT` and will read the source code from `$PATH_TO_FILES` and write a representation to`$PATH_FOR_OUTPUT`.

For example:

```bash
./bin/run.sh two_fer ~/solution-238382y7sds7fsadfasj23j/ ~/solution-238382y7sds7fsadfasj23j/output/
```

 
 [analysis]: https://github.com/exercism/automated-analysis
 [interface]: https://github.com/exercism/automated-analysis/blob/master/docs/representers/interface.md


