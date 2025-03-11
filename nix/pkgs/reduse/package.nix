{
  lib,
  python3Packages,
}:

python3Packages.buildPythonApplication {
  pname = "reduse";
  version = "0.0.1";
  pyproject = true;

  src = lib.sources.cleanSource ../../..;

  build-system = with python3Packages; [ hatchling ];

  dependencies = with python3Packages; [
    requests
    typer
    pyyaml
  ];

  meta = {
    description = "A reproducibility smells detection tool ";
    homepage = "https://github.com/SMART-Dal/Ansible-Reproducibility";
    license = lib.licenses.asl20;
    mainProgram = "reduse";
  };
}
