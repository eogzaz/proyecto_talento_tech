import matplotlib.pyplot as plt
import seaborn as sns

def grafico_linea(df, col1, col2,pais):
    """
    Generates a line plot from two columns of a DataFrame with an automatically generated title and axis labels.

    Args:
        df (pd.DataFrame): The DataFrame containing the data.
        col1 (str): The name of the column for the x-axis.
        col2 (str): The name of the column for the y-axis.
    """
    fig=plt.figure(figsize=(10, 6))
    sns.set(style="darkgrid")
    sns.lineplot(data=df, x=col1, y=col2)

    # Generate title and labels automatically
    title = f'{col1} vs {col2} en {pais}'
    xlabel = col1
    ylabel = col2

    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.grid(True)
    
    return fig

def grafico_dispersion(df, col1, col2,pais):
    """
    Generates a scatter plot from two columns of a DataFrame with an automatically generated title and axis labels.

    Args:
        df (pd.DataFrame): The DataFrame containing the data.
        col1 (str): The name of the column for the x-axis.
        col2 (str): The name of the column for the y-axis.
    """
    fig=plt.figure(figsize=(10, 6))
    sns.set(style="darkgrid")
    sns.scatterplot(data=df, x=col1, y=col2)

    # Generate title and labels automatically
    title = f'{col1} vs {col2} en {pais}'
    xlabel = col1
    ylabel = col2

    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.grid(True)
    
    return fig

def grafico_tiempo(paises, col, inicio, final, pais):

    fig=plt.figure(figsize=(10, 6))
    for indice,nombres in enumerate(paises):
        plt.plot(nombres['Tiempo [años]'], nombres[col], label=pais[indice])

    # Generate title and labels automatically
    title = f'Tiempo [años] vs {col}' #en {pais}'
    xlabel = 'Tiempo [años]'
    ylabel = col

    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.legend()
    plt.xlim(inicio,final)

    plt.grid(True)
    
    return fig
