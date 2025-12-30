FROM odoo:17

USER root
RUN apt-get update && apt-get install -y libgl1-mesa-glx
RUN apt-get install -y libleptonica-dev tesseract-ocr libtesseract-dev python3-pil tesseract-ocr-eng tesseract-ocr-script-latn
RUN apt-get update && \
    apt-get install -y \
        tesseract-ocr \
        tesseract-ocr-eng \
        libtesseract-dev && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*
RUN pip3 install --upgrade pip && \
    pip3 install opencv-python-headless
RUN pip3 install pytesseract tesseract pdf2image opencv-python matplotlib numpy pandas arabic-reshaper attrs beautifulsoup4 cffi charset-normalizer contourpy cycler docopt et-xmlfile fonttools lxml_html_clean matplotlib maxminddb numpy openpyxl python-bidi python-magic python-stdnum requests-file requests-toolbelt setuptools six soupsieve zope.event zope.interface typing_extensions
RUN apt-get -y install libsm6 libxext6
RUN apt-get update && apt-get install -y poppler-utils
RUN apt-get update && apt-get install -y wget tar libsm6 libxext6 \
    && wget https://johnvansickle.com/ffmpeg/releases/ffmpeg-release-amd64-static.tar.xz \
    && tar -xvf ffmpeg-release-amd64-static.tar.xz \
    && cp ffmpeg-*-static/ffmpeg /usr/local/bin/ \
    && cp ffmpeg-*-static/ffprobe /usr/local/bin/ \
    && rm -rf ffmpeg-*-static ffmpeg-release-amd64-static.tar.xz

EXPOSE 8069

ENTRYPOINT ["/entrypoint.sh"]
CMD ["odoo"]
