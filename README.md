# Project Overview
This repository is dedicated to the search for Tri-Nucleon decay in CUORE (Cryogenic Underground Observatory for Rare Events). It utilizes a 3D Convolutional Neural Network to search for shower-like high energy and high multiplicty events based on event topolgy within the CUORE crystal array, with linear muons tracks as the background.

This repository contains three main components for handling test data, preparing training datasets, training models, and performing statistical analysis. The workflow is structured into three main directories:

1. **DataPreparation** - Responsible for staging and preprocessing test data.
2. **Simulation** - Handles data generation using Geant4 Monte Carlo simulations and trains machine learning models.
3. **StatAnalysis** - Performs hypothesis testing and evaluates the performance of trained models.

---

## Directory Structure

```
.
├── DataPreparation/   # Prepares and preprocesses test data
├── Simulation/        # Generates training data & trains models
├── StatAnalysis/      # Analyzes model performance and hypothesis testing
├── README.md          # Project documentation
├── setup.sh           #Setting up environmental variables  
```

---

## Installation

To use this repository, ensure you have the necessary dependencies installed. It is recommended to use a virtual environment.

```bash
# Create and activate a virtual environment (optional but recommended)
python -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

---

## Usage

### Data Preparation
Navigate to the `DataPreparation/` directory and run the necessary preprocessing scripts to stage test data.

### Simulation and Model Training
Run the Geant4 Monte Carlo simulation scripts and model training within the `Simulation/` directory.

### Statistical Analysis
Use the `StatAnalysis/` directory to evaluate model performance and perform hypothesis testing.

---

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## Contact

For any inquiries or collaboration opportunities, feel free to open an issue or reach out to the maintainers.

