FROM python:3.8.3

COPY ./requirements.txt ./
COPY ./custeio.py ./

RUN mkdir data

RUN wget https://www.dropbox.com/s/gx4nh13nm8rcifc/analise-custeio-v11-3-2015-2012.csv -P data
RUN wget https://www.dropbox.com/s/th20fsu89ao8e1j/analise-custeio-v11-3-2019-2016.csv -P data


RUN pip install -r requirements.txt

EXPOSE 8501

CMD ["streamlit", "run", "custeio.py"]