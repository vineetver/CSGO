<h2 align="center">CS:GO</h2>

**Counter-Strike**: Global Offensive is the crown jewel of esports. It is a highly competitive first-person shooter game with a skill ceiling so high that only a handful of professional gamers can hit it. Every match is a battle of wits, strategies and aim, with both teams vying for victory. The very reason why CS:GO is so captivating to watch and keeps breaking viewership records. 

What makes a player great in CS:GO? Is it aim? Communication? Experience? Or is it the ability to think ten steps ahead of the enemy and always be one step forward? I aim to answer all these questions and more through a dataset of every professional CS:GO match played since 2015, which I scraped from HLTV.org. The dataset contains players' statistics, teams, events and matches.

## Setting up the environment

```bash
python -m venv venv
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
```

## Serving

### Command Line

- #### Scraping
Run scraping jobs to get the latest data from HLTV.org.

```bash
python main/scraper.py get-team-ranking
python main/scraper.py get-player-stats 
python main/scraper.py get_detailed_player_stats 
```

## About the Data

| Column Name            | Description                                                                                                                                                                                                                                                 |
|-----------------------|-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|


## Model Wrapper

`src/models/classifiers.py` contains the wrapper for the models.
The wrapper is used to train and test the models. Any model can be added and tested against the data without any changes to current code.

Here is the code for  an abstract class that implements the wrapper.

```python
class Model(ABC):
    """Abstract class for models."""
    def __init__(self, features: List[str] = None, label: str = None, params: dict = None):
        if features is None:
            features = []
        if label is None:
            label = []
        if params is None:
            params = {}
        self.label = label
        self.features = features
        self.params = params
        self.model = None

    def preprocess(self, df: pd.DataFrame):
        """ Any model specific preprocessing that needs to be done before training the model."""
        pass

    def split(self, X, Y, test_size: float):
        """Split the data into training and test sets."""
        pass

    def normalize(self, X):
        """Normalize the data."""
        pass

    @abstractmethod
    def fit(self, X, Y):
        """Train the model."""
        pass

    @abstractmethod
    def predict(self, X):
        """Predict the labels for the given data."""
        pass

    @abstractmethod
    def evaluate(self, X, Y):
        """Evaluate the model."""
        pass

    @abstractmethod
    def cross_validate(self, X, Y, n_splits: int = 10):
        """Cross validate the model."""
        pass

    def feature_importance(self, X, Y):
        """Get the feature importance."""
        pass
```


## Dependencies

    $ pip install -r requirements.txt


## Running the pipeline

    ---

## Running the tests

    py.test tests
    
## License

Distributed under the MIT License. See `LICENSE.md` for more information.


## Contact

Vineet Verma - vineetver@hotmail.com - [Goodbyeweekend.io](https://www.goodbyeweekend.io/)
