from shiny import App, ui, render
from pathlib import Path


import pandas as pd
import seaborn as sns
import os 

# set environment
os.environ["TOKENIZERS_PARALLELISM"] = "false"
sns.set_palette(["#8E59FF", "#E4D7FF", "#2C154D"])

### Load data#___________________________________________________________________________
root_path = "./data/"
study = '20241101 tech in city safety'
exp_name = '002b5816-8f4d-43ed-94b2-6e69198db438'

dr_name = study + '/'
dr_path = root_path + dr_name
tf_name = "Typeform responses.csv"
tf_path = dr_path + 'typeform/' + tf_name

exp_name_ = exp_name + "/"

# ## Load data
dt_path = root_path + dr_name + exp_name_

file_path = './data/demo.csv'
if os.path.isfile(file_path):
    print('Reading file...')
    demo = pd.read_csv(file_path)
else:
    print('No demo.csv file found!')
    
demo = demo.set_index('participant_id', drop=False)

# Check for duplicate columns
if demo.columns.duplicated().any():
    print("Duplicate columns found:", demo.columns[demo.columns.duplicated()])
    # Remove duplicate columns
    demo = demo.loc[:, ~demo.columns.duplicated()]

# Check for duplicate index
if demo.index.duplicated().any():
    print("Duplicate index found:", demo.index[demo.index.duplicated()])
    # Remove duplicate index
    demo = demo[~demo.index.duplicated()]

# ______________________________________________________________________
#### BUILD APPLICATION ### 
app_ui = ui.page_fluid(
    ui.card(
        ui.card_header("Demographics"),
        ui.layout_sidebar(
        ui.sidebar(
                ui.input_checkbox_group(
                    "demographics", 
                    "Choose up to 2 demographics to plot",
                    {
                        "Age":ui.span("Age"),
                        "Political affiliation (uk)":ui.span("Political affiliation"), 
                        "Sex":ui.span("Sex"),
                        "Ethnicity simplified":ui.span("Ethnicity"),
                    }, 
                    selected=["Age", "Political affiliation (uk)"]
                    ),
                ),   
            ui.output_plot("plot_demographics_hist"),
            ),
        full_screen=True, 
        ),
)


### SERVER ###________________________________________________________________________

def server(input, output, session):    
    @output
    @render.plot
    def plot_demographics_hist():
       if len(input.demographics()) == 0:
          return 
       elif len(input.demographics()) == 1:
          return sns.histplot(data=demo, x=input.demographics()[0], multiple="dodge")
       else:
          return sns.histplot(data=demo, x=input.demographics()[0], hue=input.demographics()[1], multiple="dodge")


app_dir = Path(__file__).parent
print(app_dir)
# This is a shiny.App object. It must be named `app`.
app = App(app_ui, server=server, static_assets=app_dir / "www")