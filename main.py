from flask import Flask, render_template_string, request
import plotly.graph_objs as go
import plotly.utils
import json

app = Flask(__name__)

HTML = """
<!DOCTYPE html>
<html>
<head>
    <title>Compound Interest Calculator</title>
    <script src="https://cdn.plot.ly/plotly-latest.min.js"></script>
    <style>
        body { font-family: Arial, sans-serif; margin: 40px; max-width: 1200px; }
        input, select { margin: 5px; padding: 5px; }
        .result { margin-top: 20px; font-size: 1.2em; }
        .chart-container { margin-top: 30px; }
        .form-container { background: #f5f5f5; padding: 20px; border-radius: 8px; margin-bottom: 20px; }
        .table-container { margin-top: 30px; }
        .breakdown-table { 
            width: 100%; 
            border-collapse: collapse; 
            margin-top: 15px;
            background: white;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
            border-radius: 8px;
            overflow: hidden;
        }
        .breakdown-table th { 
            background-color: #007cba; 
            color: white; 
            padding: 12px; 
            text-align: right;
            font-weight: bold;
        }
        .breakdown-table th:first-child { text-align: center; }
        .breakdown-table td { 
            padding: 10px 12px; 
            border-bottom: 1px solid #eee; 
            text-align: right;
        }
        .breakdown-table td:first-child { 
            text-align: center; 
            font-weight: bold;
            background-color: #f8f9fa;
        }
        .breakdown-table tr:hover { 
            background-color: #f5f5f5; 
        }
        .breakdown-table tr:last-child td { 
            border-bottom: none; 
        }
    </style>
</head>
<body>
    <h1>Compound Interest Calculator</h1>
    
    <div class="form-container">
        <form method="POST">
            <label>Initial amount: €</label>
            <input type="number" name="principal" value="{{ form_values.principal }}"><br>
            
            <label>Years:</label>
            <input type="number" name="years" value="{{ form_values.years }}"><br>
            
            <label>Rate (%):</label>
            <input type="number" step="0.01" name="rate" value="{{ form_values.rate }}"><br>
            
            <label>Recurring contribution: €</label>
            <input type="number" name="contrib" value="{{ form_values.contrib }}"><br>
            
            <label>Contribution frequency:</label>
            <select name="contrib_frequency">
                <option value="1" {% if form_values.contrib_frequency == "1" %}selected{% endif %}>Annually</option>
                <option value="12" {% if form_values.contrib_frequency == "12" %}selected{% endif %}>Monthly</option>
            </select><br>
            
            <label>Compound frequency:</label>
            <select name="compound_frequency">
                <option value="1" {% if form_values.compound_frequency == "1" %}selected{% endif %}>Annually</option>
                <option value="12" {% if form_values.compound_frequency == "12" %}selected{% endif %}>Monthly</option>
            </select><br>
            
            <input type="submit" value="Calculate" style="margin-top: 10px; padding: 10px 20px; background-color: #007cba; color: white; border: none; border-radius: 4px; cursor: pointer;">
        </form>
    </div>
    
    {% if result %}
    <div class="result">
        <h3>Results:</h3>
        <p><strong>Final Balance:</strong> €{{ result["total"] }}</p>
        <p>Total Contributed: €{{ result["contributed"] }}</p>
        <p>Interest Earned: €{{ result["interest"] }}</p>
    </div>
    
    <div class="table-container">
        <h3>Year-by-Year Breakdown:</h3>
        <table class="breakdown-table">
            <thead>
                <tr>
                    <th>Year</th>
                    <th>Balance BoY</th>
                    <th>Yearly Contributed</th>
                    <th>Yearly Interest Earned</th>
                    <th>Balance EoY</th>
                </tr>
            </thead>
            <tbody>
                {% for row in result.table_data %}
                <tr>
                    <td>{{ row.year }}</td>
                    <td>€{{ row.balance_boy }}</td>
                    <td>€{{ row.new_yearly_contributions }}</td>
                    <td>€{{ row.interest_earned }}</td>
                    <td>€{{ row.balance_eoy }}</td>
                </tr>
                {% endfor %}
            </tbody>
        </table>
    </div>
    
    <div class="chart-container">
        <div id="chart" style="width:100%; height:500px;"></div>
    </div>
    
    <script>
        var graphData = {{ chart_json|safe }};
        Plotly.newPlot('chart', graphData.data, graphData.layout);
    </script>
    {% endif %}
</body>
</html>
"""

@app.route("/", methods=["GET", "POST"])
def calculator():
    result = None
    chart_json = None
    form_values = {
        "principal": "20000",
        "years": "10", 
        "rate": "10",
        "contrib": "700",
        "compound_frequency": "1",  # Default to annual compounding
        "contrib_frequency": "12"   # Default to monthly contributions
    }
    
    if request.method == "POST":
        # Store form values to maintain them after submission
        form_values = {
            "principal": request.form["principal"],
            "years": request.form["years"],
            "rate": request.form["rate"],
            "contrib": request.form["contrib"],
            "compound_frequency": request.form["compound_frequency"],
            "contrib_frequency": request.form["contrib_frequency"]
        }
        
        P = float(request.form["principal"])
        total_years = int(request.form["years"])
        r = float(request.form["rate"]) / 100
        periodic_contribution = float(request.form["contrib"])
        n_compounds_per_year = int(request.form["compound_frequency"])  # compounding frequency
        n_contrib_per_year = int(request.form["contrib_frequency"])    # contribution frequency
        


        # Year 0 data
        balance_begining_of_year = P
        new_yearly_contribution = n_contrib_per_year * periodic_contribution
        yearly_interest_earned = round(balance_begining_of_year * r, 2)
        balance_end_of_year = balance_begining_of_year + yearly_interest_earned + new_yearly_contribution

        # Track data for graphing
        year_data = [1]
        balance_boy_data = [balance_begining_of_year]
        contributed_data = [new_yearly_contribution + P]
        interest_data = [yearly_interest_earned]
        balance_eoy_data = [balance_end_of_year]
        

        total_contributed = P
        # Calculate for each year
        for year_i in range(2, total_years + 1):

            # Calculate beginning of year balance
            balance_begining_of_year = balance_eoy_data[-1]

            # Calculate interest and end of year balance
            yearly_interest_earned = round(balance_begining_of_year * r, 2)
            balance_end_of_year = balance_begining_of_year + yearly_interest_earned + new_yearly_contribution

            total_contributed += new_yearly_contribution

            # Store yearly data
            year_data.append(year_i)
            balance_boy_data.append(balance_begining_of_year)
            contributed_data.append(total_contributed)
            interest_data.append(yearly_interest_earned)
            balance_eoy_data.append(balance_end_of_year)

        final_balance = balance_eoy_data[-1]
        final_interest = balance_eoy_data[-1] - total_contributed

        # Create table data for yearly breakdown
        table_data = []
        for i in range(len(year_data)):
            table_data.append({
                "year": year_data[i],
                "balance_boy": f"{balance_boy_data[i]:,.2f}",
                "new_yearly_contributions": f"{contributed_data[i]:,.2f}",
                "interest_earned": f"{interest_data[i]:,.2f}",
                "balance_eoy": f"{balance_eoy_data[i]:,.2f}"
            })
        
        result = {
            "total": f"{final_balance:,.2f}",
            "contributed": f"{total_contributed:,.2f}",
            "interest": f"{final_interest:,.2f}",
            "table_data": table_data
        }

        # Create Plotly chart
        fig = go.Figure()

        # Add traces
        fig.add_trace(go.Scatter(
            x=year_data,
            y=contributed_data,
            mode='lines',
            name='Total Contributions',
            line=dict(color='#1f77b4'),
            fill='tonexty'
        ))
        
        # fig.add_trace(go.Scatter(
        #     x=year_data,
        #     y=interest_data,
        #     mode='lines',
        #     name='Interest Earned',
        #     line=dict(color='#ff7f0e'),
        #     fill='tonexty'
        # ))
        
        fig.add_trace(go.Scatter(
            x=year_data,
            y=balance_eoy_data,
            mode='lines+markers',
            name='Total Balance',
            line=dict(color='#2ca02c', width=3),
            marker=dict(size=6)
        ))
        
        fig.update_layout(
            title='Compound Interest Growth Over Time',
            xaxis_title='Years',
            yaxis_title='Amount (€)',
            hovermode='x unified',
            template='plotly_white',
            height=500
        )
        
        # Format x-axis to start at 1 and show integer ticks
        fig.update_xaxes(
            range=[1, max(year_data)],
            tick0=1,
            dtick=1
        )
        
        # Format y-axis as currency
        fig.update_yaxes(tickformat='€,.0f')
        
        # Convert to JSON
        chart_json = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    
    return render_template_string(HTML, result=result, chart_json=chart_json, form_values=form_values)

if __name__ == "__main__":
    app.run(debug=True)