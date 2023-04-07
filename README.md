# Exercism Python Representer

An [automated analysis][analysis] tool that parses a Python file to create a normalized `representation.txt` file per the [representer interface][interface].


# Creating A Representation


The Representer is run with `./bin/run.sh` `<exercise-slug>` `<path/to/solution/dir/` `</path/to/output/dir/>` and will read the source code from `<path/to/solution/dir/>` and write a representation to`</path/to/output/dir/>`.


For example:

```bash
./bin/run.sh two_fer ~/solution-238382y7sds7fsadfasj23j/ ~/solution-238382y7sds7fsadfasj23j/output/
```


**Please Note**:  When using the `run-in-docker.sh` script, the paths `<path/to/solution/dir/>` and `</path/to/output/dir/>` need to be _**relative**_ to the location of this repo in your local environment.


For example:

```bash
./bin/run-in-docker.sh acronym ../python/exercises/practice/acronym/ ../python/exercises/practice/acronym/
```

Either of these commands/methods should produce the following three files in `</path/to/output/dir/>`:

1.  `mapping.json`, which maps the variable names to their placeholder values.
2.  `representation.out` - an AST representation of the solution code.
3.  `representation.txt` - the transformed solution code with placeholders.



# Running the Tests for the Representer

To run all of the current tests:

1. Ensure you have a copy of `pytest 7.2.2` installed globally, or in a virtual env.
2. Ensure you have Python 3.11.2 installed globally, or in a virtual env.
3. Open a terminal in the root of your local copy of this project.
4. Run `pytest` or `pytest -v`


 [analysis]: https://github.com/exercism/automated-analysis
 [interface]: https://github.com/exercism/automated-analysis/blob/master/docs/representers/interface.md

