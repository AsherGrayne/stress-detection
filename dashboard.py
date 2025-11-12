"""
Real-time Dashboard for Sensor Data and Stress Prediction
Displays sensor readings and predictions from all models
"""
import dash
from dash import dcc, html, Input, Output
import plotly.graph_objs as go
import pandas as pd
import json
import os
from datetime import datetime
import time
from predict import load_model, predict_single_point
from firebase_config import initialize_firebase, save_stress_event, get_stress_events

# Configuration
DATA_FILE = "sensor_data.json"
TRAINING_DATA_FILE = "balanced_data.csv"
MODELS_DIR = "models"
UPDATE_INTERVAL = 1000  # milliseconds

# Track current row in dataset
_current_row_index = 0
_training_data = None
# Accumulate historical data for graphs
_data_history = pd.DataFrame()

# Load all available models
def load_all_models():
    """Load all joblib models from models directory"""
    models = {}
    if os.path.exists(MODELS_DIR):
        model_files = [f for f in os.listdir(MODELS_DIR) if f.endswith('.joblib')]
        for model_file in model_files:
            model_name = model_file.replace('.joblib', '')
            try:
                print(f"Loading model: {model_name}")
                models[model_name] = load_model(model_file, model_dir=MODELS_DIR)
                print(f"  ✓ Loaded successfully")
            except Exception as e:
                print(f"  ✗ Failed to load: {e}")
    return models

# Load training dataset function (must be defined before use)
def load_training_dataset():
    """Load training dataset from CSV file"""
    global _training_data
    if _training_data is None:
        if os.path.exists(TRAINING_DATA_FILE):
            print(f"Loading training data from {TRAINING_DATA_FILE}...")
            _training_data = pd.read_csv(TRAINING_DATA_FILE)
            print(f"Loaded {len(_training_data)} rows")
        else:
            print(f"Warning: {TRAINING_DATA_FILE} not found")
            _training_data = pd.DataFrame()
    return _training_data

def get_current_row():
    """Get current row from training dataset"""
    global _current_row_index, _training_data
    
    if _training_data is None:
        load_training_dataset()
    
    if _training_data.empty:
        return None
    
    # Get current row (wrap around if we reach the end)
    row = _training_data.iloc[_current_row_index % len(_training_data)]
    
    # Increment for next time
    _current_row_index = (_current_row_index + 1) % len(_training_data)
    
    return row

# Load models at startup
print("Loading ML models...")
MODELS = load_all_models()
print(f"Loaded {len(MODELS)} models: {list(MODELS.keys())}\n")

# Load training dataset at startup
print("Loading training dataset...")
load_training_dataset()
if _training_data is not None and not _training_data.empty:
    print(f"Ready to process {len(_training_data)} rows from {TRAINING_DATA_FILE}\n")
else:
    print(f"Warning: No training data loaded\n")

# Initialize Firebase (optional)
FIREBASE_ENABLED = os.getenv('FIREBASE_ENABLED', 'false').lower() == 'true'
FIREBASE_CREDENTIAL = os.getenv('FIREBASE_CREDENTIAL', 'firebase_credentials.json')
if FIREBASE_ENABLED:
    print("Initializing Firebase...")
    initialize_firebase(credential_path=FIREBASE_CREDENTIAL)
    print("Firebase initialized\n")
else:
    print("Firebase disabled. Set FIREBASE_ENABLED=true to enable.\n")

# Initialize Dash app
app = dash.Dash(__name__)
app.title = "Sensor Data & Stress Prediction Dashboard"

# Add custom CSS for animations
app.index_string = '''
<!DOCTYPE html>
<html>
    <head>
        {%metas%}
        <title>{%title%}</title>
        {%favicon%}
        {%css%}
        <style>
            @keyframes pulse {
                0%, 100% { opacity: 1; }
                50% { opacity: 0.5; }
            }
        </style>
    </head>
    <body>
        {%app_entry%}
        <footer>
            {%config%}
            {%scripts%}
            {%renderer%}
        </footer>
    </body>
</html>
'''

# Dark theme colors
DARK_BG = '#0d1117'
CARD_BG = '#161b22'
BORDER_COLOR = '#30363d'
TEXT_PRIMARY = '#c9d1d9'
TEXT_SECONDARY = '#8b949e'
ACCENT_BLUE = '#58a6ff'
ACCENT_GREEN = '#3fb950'
ACCENT_ORANGE = '#d29922'
ACCENT_RED = '#f85149'

# App layout with dark theme
app.layout = html.Div([
    # Main container
    html.Div([
        # Header
        html.Div([
            html.H1("Real-time Sensor Data & Stress Prediction Dashboard", 
                    style={
                        'textAlign': 'center', 
                        'color': TEXT_PRIMARY, 
                        'marginBottom': '10px',
                        'fontSize': '32px',
                        'fontWeight': '600',
                        'letterSpacing': '0.5px'
                    }),
            html.Div(id='status-indicator', style={'textAlign': 'center', 'marginBottom': '30px'})
        ], style={
            'backgroundColor': CARD_BG,
            'padding': '25px',
            'borderRadius': '12px',
            'marginBottom': '25px',
            'boxShadow': '0 4px 6px rgba(0, 0, 0, 0.3)'
        }),
        
        # Model predictions section
        html.Div([
            html.H2("Model Predictions", style={
                'textAlign': 'center', 
                'color': TEXT_PRIMARY,
                'fontSize': '24px',
                'fontWeight': '500',
                'marginBottom': '20px',
                'letterSpacing': '0.3px'
            }),
            html.Div(id='predictions-display', style={
                'display': 'grid',
                'gridTemplateColumns': 'repeat(auto-fit, minmax(280px, 1fr))',
                'gap': '20px',
                'marginBottom': '30px'
            })
        ]),
        
        # Sensor data graphs
        html.Div([
            html.H2("Sensor Data", style={
                'textAlign': 'center', 
                'color': TEXT_PRIMARY,
                'fontSize': '24px',
                'fontWeight': '500',
                'marginTop': '30px',
                'marginBottom': '25px',
                'letterSpacing': '0.3px'
            }),
            
            # Accelerometer (X, Y, Z)
            html.Div([
                dcc.Graph(id='accelerometer-graph')
            ], style={
                'marginBottom': '25px',
                'backgroundColor': CARD_BG,
                'padding': '15px',
                'borderRadius': '12px',
                'boxShadow': '0 4px 6px rgba(0, 0, 0, 0.3)'
            }),
            
            # EDA, HR, TEMP
            html.Div([
                html.Div([
                    dcc.Graph(id='eda-graph')
                ], style={
                    'width': '32%', 
                    'display': 'inline-block', 
                    'padding': '10px',
                    'backgroundColor': CARD_BG,
                    'borderRadius': '12px',
                    'boxShadow': '0 4px 6px rgba(0, 0, 0, 0.3)',
                    'marginRight': '1%'
                }),
                html.Div([
                    dcc.Graph(id='hr-graph')
                ], style={
                    'width': '32%', 
                    'display': 'inline-block', 
                    'padding': '10px',
                    'backgroundColor': CARD_BG,
                    'borderRadius': '12px',
                    'boxShadow': '0 4px 6px rgba(0, 0, 0, 0.3)',
                    'marginRight': '1%'
                }),
                html.Div([
                    dcc.Graph(id='temp-graph')
                ], style={
                    'width': '32%', 
                    'display': 'inline-block', 
                    'padding': '10px',
                    'backgroundColor': CARD_BG,
                    'borderRadius': '12px',
                    'boxShadow': '0 4px 6px rgba(0, 0, 0, 0.3)'
                })
            ], style={'width': '100%', 'display': 'flex', 'flexWrap': 'wrap'})
        ])
    ], style={
        'backgroundColor': DARK_BG,
        'minHeight': '100vh',
        'padding': '30px',
        'fontFamily': '-apple-system, BlinkMacSystemFont, "Segoe UI", Helvetica, Arial, sans-serif'
    }),
    
    # Auto-refresh component
    dcc.Interval(
        id='interval-component',
        interval=UPDATE_INTERVAL,
        n_intervals=0
    )
])

def load_sensor_data():
    """Load sensor data from sensor_simulator JSON file"""
    global _data_history
    
    # Read from sensor_data.json (generated by sensor_simulator)
    if not os.path.exists(DATA_FILE):
        return _data_history
    
    try:
        with open(DATA_FILE, 'r') as f:
            all_data = json.load(f)
        
        if not all_data:
            return _data_history
        
        # Convert to DataFrame
        df_new = pd.DataFrame(all_data)
        df_new['timestamp'] = pd.to_datetime(df_new['timestamp'])
        
        # Update history with all data from JSON (keep last 100)
        _data_history = df_new.tail(100).reset_index(drop=True)
        
        return _data_history
    except Exception as e:
        print(f"Error loading sensor data: {e}")
        return _data_history

def make_predictions(sensor_data):
    """Make predictions using all loaded models"""
    if sensor_data.empty or len(MODELS) == 0:
        return {}
    
    # Get latest reading
    latest = sensor_data.iloc[-1]
    
    predictions = {}
    for model_name, model in MODELS.items():
        try:
            pred, proba = predict_single_point(
                model=model,
                X=latest['X'],
                Y=latest['Y'],
                Z=latest['Z'],
                EDA=latest['EDA'],
                HR=latest['HR'],
                TEMP=latest['TEMP'],
                datetime_str=latest['timestamp'].strftime("%Y-%m-%d %H:%M:%S")
            )
            
            predictions[model_name] = {
                'label': float(pred),
                'probabilities': proba.tolist() if proba is not None else None,
                'confidence': float(max(proba)) if proba is not None else None
            }
        except Exception as e:
            predictions[model_name] = {'error': str(e)}
    
    return predictions

@app.callback(
    [Output('status-indicator', 'children'),
     Output('predictions-display', 'children'),
     Output('accelerometer-graph', 'figure'),
     Output('eda-graph', 'figure'),
     Output('hr-graph', 'figure'),
     Output('temp-graph', 'figure')],
    Input('interval-component', 'n_intervals')
)
def update_dashboard(n):
    """Update dashboard with latest data"""
    # Load sensor data
    df = load_sensor_data()
    
    # Status indicator
    if df.empty:
        status = html.Div([
            html.Span("●", style={
                'color': ACCENT_RED, 
                'fontSize': '16px', 
                'marginRight': '10px',
                'animation': 'pulse 2s infinite'
            }),
            html.Span("Waiting for sensor data...", style={
                'fontSize': '14px', 
                'color': TEXT_SECONDARY,
                'fontWeight': '500'
            })
        ])
        predictions_cards = [html.Div("No data available", style={
            'textAlign': 'center', 
            'color': TEXT_SECONDARY,
            'padding': '20px',
            'backgroundColor': CARD_BG,
            'borderRadius': '12px',
            'border': f'1px solid {BORDER_COLOR}'
        })]
    else:
        latest_time = df.iloc[-1]['timestamp']
        # Note: actual_label won't be available from sensor_simulator data
        total_readings = len(df)
        
        status_text = f"Total readings: {total_readings} | Last update: {latest_time.strftime('%H:%M:%S')}"
        
        status = html.Div([
            html.Span("●", style={
                'color': ACCENT_GREEN, 
                'fontSize': '16px', 
                'marginRight': '10px',
                'animation': 'pulse 2s infinite'
            }),
            html.Span(status_text, 
                     style={
                         'fontSize': '14px', 
                         'color': ACCENT_GREEN,
                         'fontWeight': '500'
                     })
        ])
        
        # Make predictions
        predictions = make_predictions(df)
        
        # Create prediction cards
        predictions_cards = []
        for model_name, pred_data in predictions.items():
            if 'error' in pred_data:
                card = html.Div([
                    html.H3(model_name.replace('_', ' ').title(), 
                            style={
                                'margin': '0 0 10px 0', 
                                'color': ACCENT_RED, 
                                'fontSize': '18px',
                                'fontWeight': '600',
                                'letterSpacing': '0.3px'
                            }),
                    html.P(f"Error: {pred_data['error'][:40]}", 
                          style={
                              'margin': '5px 0', 
                              'color': TEXT_SECONDARY, 
                              'fontSize': '13px',
                              'fontFamily': 'monospace'
                          })
                ], style={
                    'border': f'1px solid {ACCENT_RED}',
                    'borderRadius': '12px',
                    'padding': '20px',
                    'backgroundColor': CARD_BG,
                    'boxShadow': '0 4px 6px rgba(0, 0, 0, 0.3)',
                    'transition': 'transform 0.2s',
                    'borderLeft': f'4px solid {ACCENT_RED}'
                })
            else:
                label = pred_data['label']
                confidence = pred_data.get('confidence', 0)
                label_colors = {0.0: ACCENT_BLUE, 1.0: ACCENT_ORANGE, 2.0: ACCENT_RED}
                label_names = {0.0: 'Low', 1.0: 'Medium', 2.0: 'High'}
                color = label_colors.get(label, TEXT_SECONDARY)
                label_name = label_names.get(label, 'Unknown')
                
                # Get actual label for comparison
                actual_label = df.iloc[-1].get('actual_label', None)
                is_correct = actual_label is not None and label == actual_label
                
                # Save to Firebase if stress detected and enabled
                if FIREBASE_ENABLED and label > 0:  # Save if stress level is 1 or 2
                    latest = df.iloc[-1]
                    sensor_data = {
                        'X': float(latest['X']),
                        'Y': float(latest['Y']),
                        'Z': float(latest['Z']),
                        'EDA': float(latest['EDA']),
                        'HR': float(latest['HR']),
                        'TEMP': float(latest['TEMP'])
                    }
                    save_stress_event(
                        stress_level=label,
                        confidence=confidence,
                        sensor_data=sensor_data,
                        model_name=model_name
                    )
                
                card = html.Div([
                    html.H3(model_name.replace('_', ' ').title(), 
                            style={
                                'margin': '0 0 15px 0', 
                                'color': TEXT_PRIMARY, 
                                'fontSize': '18px',
                                'fontWeight': '600',
                                'letterSpacing': '0.3px'
                            }),
                    html.Div([
                        html.Div([
                            html.Span("Predicted Stress Level", style={
                                'fontSize': '12px', 
                                'color': TEXT_SECONDARY,
                                'textTransform': 'uppercase',
                                'letterSpacing': '0.5px',
                                'fontWeight': '500'
                            }),
                            html.Div([
                                html.Span(f"{label_name}", 
                                        style={
                                            'fontSize': '28px', 
                                            'fontWeight': '700', 
                                            'color': color,
                                            'marginRight': '8px'
                                        }),
                                html.Span(f"({label:.0f})", 
                                        style={
                                            'fontSize': '18px', 
                                            'color': TEXT_SECONDARY,
                                            'fontWeight': '400'
                                        })
                            ], style={'marginTop': '8px'})
                        ], style={'marginBottom': '15px'}),
                        html.Div([
                            html.Span("Confidence", style={
                                'fontSize': '12px', 
                                'color': TEXT_SECONDARY,
                                'textTransform': 'uppercase',
                                'letterSpacing': '0.5px',
                                'fontWeight': '500'
                            }),
                            html.Span(f"{confidence:.1%}", 
                                    style={
                                        'fontSize': '20px', 
                                        'fontWeight': '600', 
                                        'color': ACCENT_GREEN,
                                        'display': 'block',
                                        'marginTop': '5px'
                                    })
                        ]),
                        # Show actual label if available
                        html.Div([
                            html.Span("Actual Label", style={
                                'fontSize': '12px', 
                                'color': TEXT_SECONDARY,
                                'textTransform': 'uppercase',
                                'letterSpacing': '0.5px',
                                'fontWeight': '500'
                            }),
                            html.Div([
                                html.Span(f"{label_names.get(actual_label, 'N/A')} ({actual_label:.0f})" if actual_label is not None else "N/A", 
                                        style={
                                            'fontSize': '16px', 
                                            'fontWeight': '600', 
                                            'color': label_colors.get(actual_label, TEXT_SECONDARY) if actual_label is not None else TEXT_SECONDARY,
                                            'marginRight': '8px'
                                        }),
                                html.Span("CORRECT" if is_correct else "INCORRECT", 
                                        style={
                                            'fontSize': '12px', 
                                            'fontWeight': 'bold',
                                            'color': ACCENT_GREEN if is_correct else ACCENT_RED,
                                            'padding': '2px 8px',
                                            'borderRadius': '4px',
                                            'backgroundColor': f'rgba({58 if is_correct else 248}, {166 if is_correct else 81}, {255 if is_correct else 73}, 0.2)'
                                        }) if actual_label is not None else None
                            ], style={'marginTop': '5px', 'display': 'flex', 'alignItems': 'center', 'gap': '8px'})
                        ], style={'marginTop': '10px'}) if actual_label is not None else None
                    ])
                ], style={
                    'border': f'1px solid {BORDER_COLOR}',
                    'borderLeft': f'4px solid {color}',
                    'borderRadius': '12px',
                    'padding': '20px',
                    'backgroundColor': CARD_BG,
                    'boxShadow': '0 4px 6px rgba(0, 0, 0, 0.3)',
                    'transition': 'transform 0.2s, box-shadow 0.2s',
                    'cursor': 'default'
                })
            predictions_cards.append(card)
    
    # Create graphs with dark theme
    if df.empty:
        empty_fig = go.Figure()
        empty_fig.update_layout(
            template='plotly_dark',
            plot_bgcolor=CARD_BG,
            paper_bgcolor=CARD_BG,
            font=dict(color=TEXT_PRIMARY)
        )
        empty_fig.add_annotation(
            text="No data available", 
            xref="paper", yref="paper", x=0.5, y=0.5, 
            showarrow=False,
            font=dict(size=16, color=TEXT_SECONDARY)
        )
        return status, predictions_cards, empty_fig, empty_fig, empty_fig, empty_fig
    
    # Get last 100 points for display
    df_display = df.tail(100).copy()
    
    # Common dark theme layout
    dark_layout = {
        'template': 'plotly_dark',
        'plot_bgcolor': CARD_BG,
        'paper_bgcolor': CARD_BG,
        'font': dict(color=TEXT_PRIMARY, size=12),
        'xaxis': dict(
            gridcolor=BORDER_COLOR,
            linecolor=BORDER_COLOR,
            showgrid=True
        ),
        'yaxis': dict(
            gridcolor=BORDER_COLOR,
            linecolor=BORDER_COLOR,
            showgrid=True
        ),
        'hovermode': 'x unified',
        'hoverlabel': dict(
            bgcolor='rgba(0, 0, 0, 0.8)',
            font_size=12,
            font_family="monospace"
        )
    }
    
    # Accelerometer graph
    accel_fig = go.Figure()
    accel_fig.add_trace(go.Scatter(
        x=df_display['timestamp'], 
        y=df_display['X'], 
        name='X', 
        line=dict(color='#f85149', width=2),
        mode='lines'
    ))
    accel_fig.add_trace(go.Scatter(
        x=df_display['timestamp'], 
        y=df_display['Y'], 
        name='Y', 
        line=dict(color='#58a6ff', width=2),
        mode='lines'
    ))
    accel_fig.add_trace(go.Scatter(
        x=df_display['timestamp'], 
        y=df_display['Z'], 
        name='Z', 
        line=dict(color='#3fb950', width=2),
        mode='lines'
    ))
    accel_fig.update_layout(
        title=dict(
            text='Accelerometer (X, Y, Z)',
            font=dict(size=18, color=TEXT_PRIMARY),
            x=0.5
        ),
        xaxis_title='Time',
        yaxis_title='Value',
        **dark_layout,
        height=400,
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1,
            bgcolor='rgba(0,0,0,0)',
            bordercolor=BORDER_COLOR
        )
    )
    
    # EDA graph
    eda_fig = go.Figure()
    eda_fig.add_trace(go.Scatter(
        x=df_display['timestamp'], 
        y=df_display['EDA'], 
        name='EDA', 
        line=dict(color='#a371f7', width=2),
        fill='tozeroy',
        fillcolor='rgba(163, 113, 247, 0.2)',
        mode='lines'
    ))
    eda_fig.update_layout(
        title=dict(
            text='Electrodermal Activity (EDA)',
            font=dict(size=16, color=TEXT_PRIMARY),
            x=0.5
        ),
        xaxis_title='Time',
        yaxis_title='EDA',
        **dark_layout,
        height=300,
        showlegend=False
    )
    
    # Heart Rate graph
    hr_fig = go.Figure()
    hr_fig.add_trace(go.Scatter(
        x=df_display['timestamp'], 
        y=df_display['HR'], 
        name='Heart Rate', 
        line=dict(color='#d29922', width=2),
        fill='tozeroy',
        fillcolor='rgba(210, 153, 34, 0.2)',
        mode='lines'
    ))
    hr_fig.update_layout(
        title=dict(
            text='Heart Rate (HR)',
            font=dict(size=16, color=TEXT_PRIMARY),
            x=0.5
        ),
        xaxis_title='Time',
        yaxis_title='BPM',
        **dark_layout,
        height=300,
        showlegend=False
    )
    
    # Temperature graph
    temp_fig = go.Figure()
    temp_fig.add_trace(go.Scatter(
        x=df_display['timestamp'], 
        y=df_display['TEMP'], 
        name='Temperature', 
        line=dict(color='#f85149', width=2),
        fill='tozeroy',
        fillcolor='rgba(248, 81, 73, 0.2)',
        mode='lines'
    ))
    temp_fig.update_layout(
        title=dict(
            text='Temperature (TEMP)',
            font=dict(size=16, color=TEXT_PRIMARY),
            x=0.5
        ),
        xaxis_title='Time',
        yaxis_title='°C',
        **dark_layout,
        height=300,
        showlegend=False
    )
    
    return status, predictions_cards, accel_fig, eda_fig, hr_fig, temp_fig

if __name__ == '__main__':
    print("\n" + "="*60)
    print("Starting Dashboard...")
    print("="*60)
    print(f"Dashboard URL: http://127.0.0.1:8050")
    print(f"Data source: {DATA_FILE} (from sensor_simulator.py)")
    print(f"Update interval: {UPDATE_INTERVAL}ms")
    print("\nMake sure to run sensor_simulator.py to generate data!")
    print("="*60 + "\n")
    
    app.run_server(debug=True, host='0.0.0.0', port=8050)

