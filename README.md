# Compound Interest Calculator

A web-based compound interest calculator built with Flask and Plotly that helps you visualize how your investments grow over time.

## Features

- 💰 **Interactive Calculator**: Calculate compound interest with customizable parameters
- 📊 **Visual Charts**: Interactive Plotly graphs showing growth over time
- 📋 **Detailed Breakdown**: Year-by-year table showing balance progression
- 🎛️ **Flexible Options**: 
  - Separate compound and contribution frequencies
  - Annual or monthly compounding
  - Annual or monthly contributions
- 💱 **Euro Currency**: All calculations displayed in euros (€)
- 📱 **Responsive Design**: Two-column layout with form and chart side-by-side

## The app in action

![Compound Interest Calculator Screenshot](images/img_01.png)

The calculator displays:
- Input form on the left with all parameters
- Interactive chart on the right showing growth visualization
- Detailed year-by-year breakdown table below

## Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/osomike/compound_interest_calculator.git
   cd compound_interest_calculator
   ```

2. **Create a virtual environment**:
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

## Docker Deployment

### Option 1: Using Docker Compose (Recommended)

1. **Build and run with Docker Compose**:
   ```bash
   docker-compose up --build
   ```

2. **Run in background**:
   ```bash
   docker-compose up -d --build
   ```

3. **Stop the application**:
   ```bash
   docker-compose down
   ```

### Option 2: Using Docker directly

1. **Build the Docker image**:
   ```bash
   docker build -t compound-interest-calculator .
   ```

2. **Run the container**:
   ```bash
   docker run -p 5000:5000 compound-interest-calculator
   ```

3. **Run in background**:
   ```bash
   docker run -d -p 5000:5000 --name compound-calculator compound-interest-calculator
   ```

### Docker Commands

- **View logs**: `docker-compose logs -f`
- **Stop container**: `docker-compose stop`
- **Remove container**: `docker-compose down`
- **Rebuild**: `docker-compose up --build --force-recreate`

## Usage

1. **Start the application**:
   ```bash
   python main.py
   ```

2. **Open your browser** and navigate to:
   ```
   http://127.0.0.1:5000
   ```

3. **Enter your parameters**:
   - **Initial amount**: Your starting investment (€)
   - **Years**: Investment duration
   - **Rate**: Annual interest rate (%)
   - **Recurring contribution**: Regular contribution amount (€)
   - **Contribution frequency**: How often you contribute (Annual/Monthly)
   - **Compound frequency**: How often interest compounds (Annual/Monthly)

4. **Click Calculate** to see:
   - Summary results (Final Balance, Total Contributed, Interest Earned)
   - Interactive growth chart
   - Detailed year-by-year breakdown

## Dependencies

### Python Dependencies
- **Flask**: Web framework
- **Plotly**: Interactive charting library

See `requirements.txt` for specific versions.

### Docker (Alternative)
- **Docker Engine**: Container runtime
- **Docker Compose**: For easy orchestration (optional)

## Project Structure

```
compound_interest_calculator/
├── main.py              # Main Flask application
├── requirements.txt     # Python dependencies
├── Dockerfile          # Docker container configuration
├── docker-compose.yml  # Docker Compose orchestration
├── .dockerignore       # Docker build exclusions
├── README.md           # This file
└── .venv/              # Virtual environment (created after setup)
```

## How It Works

### Compound Interest Formula

The calculator uses compound interest principles:

- **Principal**: Initial investment amount
- **Rate**: Annual interest rate
- **Time**: Investment duration in years
- **Contributions**: Regular additional investments
- **Compounding**: Interest calculated on principal + accumulated interest

### Calculation Logic

1. **Year 1**: Start with principal + first year contributions and interest
2. **Subsequent years**: Apply interest to accumulated balance + add new contributions
3. **Flexibility**: Different frequencies for contributions vs. compounding
4. **Safety limits**: Maximum 50 years to prevent performance issues

## Features in Detail

### Chart Visualization
- **Total Contributions**: Blue line showing cumulative contributions
- **Total Balance**: Green line with markers showing account growth
- **Legend**: Positioned below chart for clean layout
- **Interactive**: Hover for detailed values, zoom and pan capabilities

### Table Breakdown
- Year-by-year progression
- Beginning of year balance
- Yearly contributions added
- Interest earned each year
- End of year balance

### Form Persistence
- Input values are maintained after calculation
- Easy to experiment with different scenarios
- No need to re-enter all values for adjustments

## Development Notes

- Built with Flask for simplicity and ease of deployment
- Uses Plotly for interactive, professional-looking charts
- Responsive CSS design for desktop usage
- Debug mode enabled for development
- European currency formatting (€)

## Deployment

### Docker Deployment

The application is fully containerized and can be deployed using Docker:

1. **Prerequisites**: Install Docker and Docker Compose on your system

2. **Build and run with Docker Compose**:
   ```bash
   docker-compose up --build
   ```

3. **Access the application**:
   - Open your browser to `http://localhost:5000`
   - The application will be running in a production-ready container

4. **Stop the application**:
   ```bash
   docker-compose down
   ```

### Manual Deployment

For manual deployment without Docker:

1. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Run the application**:
   ```bash
   python main.py
   ```

3. **Access at**: `http://localhost:5000`

### Production Considerations

- The Docker setup includes health checks and security hardening
- For production deployment, consider using a reverse proxy (nginx)
- Environment variables can be configured in docker-compose.yml
- The application is designed to handle reasonable load for personal use

