"""CLI for OpenFold funcX endpoint."""
from pathlib import Path
from uuid import UUID

import typer
from funcx.sdk.client import FuncXClient
from rich import print

from funcx_openfold.utils import OpenFoldResult

app = typer.Typer()


def func(
    fasta_str: str,
    database_path: "Path",
    output_dir: "Path",
    openfold_path: "Path",
) -> "OpenFoldResult":
    """Run OpenFold.

    Parameters
    ----------
    fasta_str : str
        The raw string corresponding to the fasta file text.
    database_path : Path
        The path to the database on the cluster.
    output_dir : Path
        The path to write the results to on the cluster.
    openfold_path : Path
        The path to the OpenFold repository on the cluster.

    Return
    ------
    OpenFoldResult : Result object storing the returncode, stdout, and stderr.
    """
    import subprocess

    from funcx_openfold.utils import OpenFoldResult, write_log

    # Write the fasta file
    output_dir.mkdir(exist_ok=True)
    fasta_path = output_dir / "sequence.fasta"
    fasta_path.write_text(fasta_str)

    command = f"""python3 {openfold_path}/run_pretrained_openfold.py \
        {fasta_path} \
        {database_path}/pdb_mmcif/mmcif_files/ \
        --uniref90_database_path {database_path}/uniref90/uniref90.fasta \
        --mgnify_database_path {database_path}/mgnify/mgy_clusters_2018_12.fa \
        --pdb70_database_path {database_path}/pdb70/pdb70 \
        --uniclust30_database_path {database_path}/uniclust30/uniclust30_2018_08/uniclust30_2018_08 \
        --output_dir {output_dir} \
        --bfd_database_path {database_path}/bfd/bfd_metaclust_clu_complete_id30_c90_final_seq.sorted_opt \
        --model_device "cuda:0" \
        --jackhmmer_binary_path jackhmmer \
        --hhblits_binary_path hhblits \
        --hhsearch_binary_path hhsearch \
        --kalign_binary_path kalign
        --config_preset "model_1_ptm"
        --openfold_checkpoint_path {openfold_path}/openfold/resources/openfold_params/finetuning_ptm_2.pt"""

    # This function blocks until the job finishes
    proc = subprocess.run(command.split(), capture_output=True)

    # Process the output
    result = OpenFoldResult(
        returncode=proc.returncode,
        stdout=proc.stdout.decode("utf-8"),
        stderr=proc.stderr.decode("utf-8"),
    )
    write_log(result.stdout, output_dir / "stdout.log")
    write_log(result.stderr, output_dir / "stderr.log")

    return result


@app.command()
def register() -> None:
    """Register funcX OpenFold function and output the --function UUID."""
    fxc = FuncXClient()
    function_id = fxc.register_function(func)
    print(f"Registered OpenFold at endpoint: {function_id}")


@app.command()
def run(
    endpoint_id: UUID = typer.Option(
        ..., "--endpoint", help="UUID for cluster endpoint."
    ),
    function_id: UUID = typer.Option(
        ..., "--function", help="UUID for registered function."
    ),
    fasta_file: Path = typer.Option(
        ...,
        "-f",
        "--fasta",
        exists=True,
        file_okay=True,
        dir_okay=False,
        help="Fasta file containing sequence to fold.",
    ),
    database_path: Path = typer.Option(
        ..., "-d", "--database", help="Path to batabase on cluster."
    ),
    output_dir: Path = typer.Option(
        ..., "-o", "--output", help="Output directory on cluster."
    ),
    openfold_path: Path = typer.Option(
        ..., "--openfold", help="Path to OpenFold repository on cluster."
    ),
) -> None:
    """Run OpenFold job on a cluster to fold --fasta with a registered --function UUID."""
    fasta_str = fasta_file.read_text()

    fxc = FuncXClient()
    task_id = fxc.run(
        fasta_str,  # Total payload must be < 10MB
        database_path,
        output_dir,
        openfold_path,
        function_id=str(function_id),
        endpoint_id=str(endpoint_id),
    )

    print(f"OpenFold job submitted with task ID: {task_id}")


@app.command()
def status(task_id: UUID = typer.Argument(..., help="A task UUID.")) -> None:
    """Check the status of the a funcX task given the --task-id."""
    fxc = FuncXClient()
    print(fxc.get_result(str(task_id)))


def main() -> None:
    """Entry point for CLI."""
    app()


if __name__ == "__main__":
    main()
