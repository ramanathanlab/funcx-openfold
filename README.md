# funcx-openfold
FuncX OpenFold interface.

# Install

Please run the following commands to install:
```
git clone https://github.com/ramanathanlab/funcx-openfold.git
cd funcx-openfold
pip3 install -U pip setuptools wheel
pip3 install -r requirements/requirements.txt
pip3 install -e .
```

To test the installation and view the CLI command options:
```
funcx-openfold --help
funcx-openfold register --help
funcx-openfold run --help
funcx-openfold status --help
```

# CLI

**Usage**:

```console
$ funcx-openfold COMMAND [ARGS]...
```

**Options**:

* `--install-completion`: Install completion for the current shell.
* `--show-completion`: Show completion for the current shell, to copy it or customize the installation.
* `--help`: Show this message and exit.

**Commands**:

* `register`: Register funcX OpenFold function and output the --function UUID.
* `run`: Submit an OpenFold job to the cluster to fold --fasta with a registered --function UUID.
* `status`: Check the status of the a funcX task given the --task-id.

## `register`

Register funcX OpenFold function and output the --function UUID.

**Usage**:

```console
$ register [OPTIONS]
```

**Options**:

* `--help`: Show this message and exit.

## `run`

Submit an OpenFold job to the cluster to fold --fasta
using the registered --function UUID.

**Usage**:

```console
$ run [OPTIONS]
```

**Options**:

* `--endpoint UUID`: UUID for cluster endpoint.  [required]
* `--function UUID`: UUID for registered function.  [required]
* `-f, --fasta FILE`: Fasta file containing sequence to fold.  [required]
* `-d, --database PATH`: Path to batabase on cluster.  [required]
* `-o, --output PATH`: Output directory on cluster.  [required]
* `--openfold PATH`: Path to OpenFold repository on cluster.  [required]
* `--help`: Show this message and exit.

## `status`

Check the status of the a funcX task given the --task-id.

**Usage**:

```console
$ status [OPTIONS] TASK_ID
```

**Arguments**:

* `TASK_ID`: A task UUID.  [required]

**Options**:

* `--help`: Show this message and exit.

# Contributing

To install:
```
pip3 install -U pip setuptools wheel
pip3 install -r requirements/dev.txt
pip3 install -r requirements/requirements.txt
pip3 install -e .
```

To generate the documentation: `typer cli.py utils docs`
