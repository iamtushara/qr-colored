"""common tools"""

import torch


def check_torch_version():
    """
    Checks and prints the CUDA details
    """
    cuda_available = torch.cuda.is_available()
    print(f"CUDA available: {cuda_available}")

    if cuda_available:
        print(f"Number of CUDA devices: {torch.cuda.device_count()}")
        print(f"Current CUDA device: {torch.cuda.current_device()}")
        print(f"CUDA device name: {torch.cuda.get_device_name(0)}")
        print(f"CUDA version: {torch.version.cuda}")

        # Example of using CUDA
        device = torch.device("cuda")
        tensor = torch.randn(2, 3).to(device)
        print(f"Tensor on GPU: {tensor}")
    else:
        print(
            "CUDA is not available. "
            "Ensure that CUDA is installed correctly and that your GPU is compatible."
        )
