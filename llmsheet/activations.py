activations = {
    "ReLU": lambda x : f'=MAX(0, {str(x)})',
    "tanh": lambda x : f'=TANH({str(x)})',
    "Linear": lambda x : f'={str(x)}'
}