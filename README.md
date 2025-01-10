# Developer's Salary Prediction

## Our Team

|   **ID**   |       **Full Name**      |
|:------------:|:---------------------:|
| **21280099** | Nguyễn Công Hoài Nam  |
| **21280118** | Lê Nguyễn Hoàng Uyên  |
| **21280124** | Huỳnh Công Đức        |
| **21280125** | Trần Thị Uyên Nhi     |

## Dataset

* Use **Stack Overflow Annual Developer Survey 2023** to train model. Download the dataset at [here](https://insights.stackoverflow.com/survey)

* For Salary prediction purpose, use 11 features `Country`, `Age`, `DevType`, `EdLevel`, `YearsCodePro`, `RemoteWork`,
`LanguageHaveWorkedWith`, `DatabaseHaveWorkedWith`, `PlatformHaveWorkedWith`, `ToolsTechHaveWorkedWith`, `NEWCollabToolsHaveWorkedWith`
to predict `ConvertedCompYearly` as Salary.

## Notebooks (Reports)

* Data preprocessing and visualization: [Preprocesing_Visual.ipynb](notebooks_reports/Preprocesing_Visual.ipynb)

* Modeling: [Model.ipynb](notebooks_reports/Model.ipynb)


## Demo

1. Website: [Salary Predict Web](https://developer-salary-prediction-project.streamlit.app/)

3. Run as local
Run code:
```
streamlit run app/app.py
```
