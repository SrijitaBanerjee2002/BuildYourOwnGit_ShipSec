# Srijita's Implementation of CodeCrafters' 'Build Your Git' Challenge.

As instructed, I completed all steps except the final 2 (till "Write a Tree Object"). 

# Testing locally

The `your_program.sh` script is expected to operate on the `.git` folder inside
the current working directory. If running this inside the root of this
repository, you might end up accidentally damaging your repository's `.git`
folder.

Codecrafters suggest executing `your_program.sh` in a different folder when testing
locally. For example:

```sh
mkdir -p /tmp/testing && cd /tmp/testing
/path/to/your/repo/your_program.sh init
```

To make this easier to type out, you could add a
[shell alias](https://shapeshed.com/unix-alias/):

```sh
alias mygit=/path/to/your/repo/your_program.sh

mkdir -p /tmp/testing && cd /tmp/testing
mygit init
```
