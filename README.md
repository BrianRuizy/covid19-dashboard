# Covid 19 Interactive Dashboard
###### Don't forget to leave a [star ⭐!](https://github.com/BrianRuizy/covid19-dashboard/stargazers?after=Y3Vyc29yOnYyOpO5MjAyMC0wNS0xM1QwOTo1MzoyMC0wNTowMADODRbOpg%3D%3D)

[![Awesome](https://awesome.re/badge.svg)](https://github.com/soroushchehresa/awesome-coronavirus#applications-and-bots)
[![Gitter chat](https://img.shields.io/badge/Chat-Gitter-ff69b4.svg?label=Chat&logo=gitter)](https://gitter.im/ncov-dashboard/community)
[![Build Status](https://img.shields.io/travis/TheAlgorithms/Python.svg?label=Travis%20CI&logo=travis)](https://travis-ci.com/github/BrianRuizy/covid19-dashboard)
[![MIT License](https://camo.githubusercontent.com/a307f74a14e41e762300323414ddef81f3d53ae2/68747470733a2f2f696d672e736869656c64732e696f2f6769746875622f6c6963656e73652f736f757263657265722d696f2f736f757263657265722d6170702e7376673f636f6c6f72423d666630303030)](https://github.com/BrianRuizy/covid19-dashboard/blob/master/LICENSE.md)
[![Made with Pthon](https://img.shields.io/badge/Made%20with-Python-1f425f.svg)](https://www.python.org/)

![covid-dashboard-3-devices](https://user-images.githubusercontent.com/23439187/115303139-de94f580-a128-11eb-9028-3144d808ac00.png)

## About

> Coronavirus disease (COVID-19) is an infectious disease caused by a newly discovered coronavirus.
> At this time, there are no specific vaccines or treatments for COVID-19. The best way to prevent and slow down transmission is be **well informed** about the COVID-19 virus. [who.int](https://www.who.int/health-topics/coronavirus#tab=tab_1)

The goal of this project is not to build *just another dashboard*. But, to focus on collaborative plot ideas, and a mobile friendly UI/UX. Feel free to open an issue requesting a type of plot, table, or any feature for that matter. Join the repo's [Gitter chat](https://gitter.im/ncov-dashboard/community?utm_source=share-link&utm_medium=link&utm_campaign=share-link).

[![read blog](https://brianruizy.com/favicons/favicon-32x32.png)](https://brianruizy.com/how-to-create-a-covid-19-dashboard-web-application-with-python) 
Read [blog](https://brianruizy.com/how-to-create-a-covid-19-dashboard-web-application-with-python) post my website

## Contributors

[![](https://sourcerer.io/fame/BrianRuizy/BrianRuizy/covid-19-dashboard/images/0)](https://sourcerer.io/fame/BrianRuizy/BrianRuizy/covid-19-dashboard/links/0)[![](https://sourcerer.io/fame/BrianRuizy/BrianRuizy/covid-19-dashboard/images/1)](https://sourcerer.io/fame/BrianRuizy/BrianRuizy/covid-19-dashboard/links/1)[![](https://sourcerer.io/fame/BrianRuizy/BrianRuizy/covid-19-dashboard/images/2)](https://sourcerer.io/fame/BrianRuizy/BrianRuizy/covid-19-dashboard/links/2)[![](https://sourcerer.io/fame/BrianRuizy/BrianRuizy/covid-19-dashboard/images/3)](https://sourcerer.io/fame/BrianRuizy/BrianRuizy/covid-19-dashboard/links/3)[![](https://sourcerer.io/fame/BrianRuizy/BrianRuizy/covid-19-dashboard/images/4)](https://sourcerer.io/fame/BrianRuizy/BrianRuizy/covid-19-dashboard/links/4)[![](https://sourcerer.io/fame/BrianRuizy/BrianRuizy/covid-19-dashboard/images/5)](https://sourcerer.io/fame/BrianRuizy/BrianRuizy/covid-19-dashboard/links/5)[![](https://sourcerer.io/fame/BrianRuizy/BrianRuizy/covid-19-dashboard/images/6)](https://sourcerer.io/fame/BrianRuizy/BrianRuizy/covid-19-dashboard/links/6)[![](https://sourcerer.io/fame/BrianRuizy/BrianRuizy/covid-19-dashboard/images/7)](https://sourcerer.io/fame/BrianRuizy/BrianRuizy/covid-19-dashboard/links/7)

## Getting Started

### Prerequisites

* Python; [pyenv](https://github.com/pyenv/pyenv) recommended
* Pip

### Installing

Get the project up and running locally in just 5 easy steps.

1. Create a personal [Fork](https://github.com/login?return_to=%2FBrianRuizy%2Fcovid19-dashboard) of this repository.

2. **Clone** the fork with HTTPS, using your local terminal to a preferred location, and **cd** into the project.

```bash
git clone https://github.com/your_username/covid19-dashboard.git

Cloning into 'covid19-dashboard'...
remote: Enumerating objects: 113, done.
remote: Counting objects: 100% (113/113), done.
remote: Compressing objects: 100% (80/80), done.
Receiving objects: 100% (2845/2845), 12.52 MiB | 5.21 MiB/s, done.

cd covid19-dashboard/
```

3. Create your virtual environment, and activate it.

```bash
python -m venv env

source env/bin/activate  # Linux/Mac
env/Scripts/activate  # Windows
```

4. Install dependencies

```bash
pip install -r requirements.txt
```

5. Run local server, and **DONE**!

```bash
python manage.py runserver

May 06, 2020 - 11:22:23
Django version 3.0.6, using settings 'core.settings'
Starting development server at http://127.0.0.1:8000/
Quit the server with CONTROL-C.
```

## Deployment

Heroku app is already configured to this repository for *automatic deploys* from any push to the **master** branch. Create a pull request containing your respective changes and wait for merge.

## Reading data locally
You can go through all the available datasets by going into the `/processdata` directory, launching a interactive python shell, importing `getdata` file, and calling any function. See below...

```bash
cd ~/repos/covid19-dashboard/processdata
```

```bash
$ python

Python 3.7.6 (default, Jan  8 2020, 20:23:39) [MSC v.1916 64 bit (AMD64)] :: Anaconda, Inc. on win32 
...

>>> import getdata
>>> getdata.realtime_growth()

         Confirmed  Deaths  Recovered
Date
1/22/20        555      17         28
1/23/20        654      18         30
...            ...     ...        ...
8/2/20    18079723  689362   10690555
8/3/20    18282208  693694   10913000

[195 rows x 3 columns]
```


## Built With

* [Django](https://www.djangoproject.com/) Django is a high-level Web framework that encourages rapid development and clean, pragmatic design.
* [Plotly](https://plotly.com/) The leading front-end for ML & data science models in Python, R, and Julia.
* [Appseed](https://appseed.us/)
* [Bootstrap](https://getbootstrap.com/)

## Data Sources

* Johns Hopkins University: [CSSE](https://systems.jhu.edu/) 2019-ncov data repository, found [here](https://github.com/CSSEGISandData/COVID-19).
* Our World in Data: [OWID](https://ourworldindata.org/) GitHub Data repository, found [here](https://github.com/owid/covid-19-data/tree/master/public/data).
* New York Times' COVID GitHub data repository, found [here](https://github.com/nytimes/covid-19-data)

## License

[@MIT](https://github.com/BrianRuizy/covid19-dashboard/blob/master/LICENSE.md)
