import typer
import subprocess
from pathlib import Path
from funcx.sdk.client import FuncXClient


app = typer.Typer()


def func(
    fasta_str: str,
    data_path: Path,
    output_dir: Path = Path("./"),
    openfold_path: Path = Path("openfold"),
) -> None:
    # TODO: What is best way to specify run_pretrained_openfold.py?
    fasta_path = Path(f"/tmp/{hash(fasta_str)}.fasta")
    fasta_path.write_text(fasta_str)
    cmd = f"""python3 run_pretrained_openfold.py \
        {fasta_path} \
        {data_path}/pdb_mmcif/mmcif_files/ \
        --uniref90_database_path {data_path}/uniref90/uniref90.fasta \
        --mgnify_database_path {data_path}/mgnify/mgy_clusters_2018_12.fa \
        --pdb70_database_path {data_path}/pdb70/pdb70 \
        --uniclust30_database_path {data_path}/uniclust30/uniclust30_2018_08/uniclust30_2018_08 \
        --output_dir {output_dir} \
        --bfd_database_path {data_path}/bfd/bfd_metaclust_clu_complete_id30_c90_final_seq.sorted_opt \
        --model_device "cuda:0" \
        --jackhmmer_binary_path jackhmmer \
        --hhblits_binary_path hhblits \
        --hhsearch_binary_path hhsearch \
        --kalign_binary_path kalign
        --config_preset "model_1_ptm"
        --openfold_checkpoint_path {openfold_path}/resources/openfold_params/finetuning_ptm_2.pt"""
    proc = subprocess.run(cmd.split(), capture_output=True)
    # This function should block until the job finishes
    # TODO: Process stdout, stderr

    # Clean up temp file
    fasta_path.unlink()


@app.command()
def register() -> None:
    fxc = FuncXClient()
    func_uuid = fxc.register_function(func)
    print(f"Registered OpenFold at endpoint: {func_uuid}")


@app.command()
def run(
    endpoint: str,
    func_uuid: str,
    fasta_file: Path,
    data_path: Path,
    output_dir: Path = Path("./"),
    openfold_path: Path = Path("openfold"),
) -> None:

    # Total payload must be < 10MB
    fasta_str = fasta_file.read_text()

    fxc = FuncXClient()
    task_id = fxc.run(
        fasta_str,
        data_path,
        output_dir,
        openfold_path,
        function_id=func_uuid,
        endpoint_id=endpoint,
    )

    print(f"OpenFold job submitted with task ID: {task_id}")


@app.command()
def status(task_id: str) -> None:
    fxc = FuncXClient()
    print(fxc.get_result(task_id))
