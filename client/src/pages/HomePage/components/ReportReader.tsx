import React, { useState } from 'react';
import { Document, Page } from 'react-pdf/dist/esm/entry.webpack';
import Button from '../../../components/Button';

const options = {
  cMapUrl: 'cmaps/',
  cMapPacked: true,
};

type IProps = {
  title?: string;
  file: any;
  download?: boolean;
}

const ReportReader = ({title, file, download = false} : IProps) => {
  const [numPages, setNumPages] = useState(null);

  const onDocumentLoadSuccess = ({ numPages: nextNumPages } : any) => {
    setNumPages(nextNumPages);
  }

  const handleDownload = () => {
    window.open(file);
  }

  return (
    <div className="pdf-container">
      {!!title && <h1>{title}</h1>}
      <Document
        file={file}
        onLoadSuccess={onDocumentLoadSuccess}
        options={options}
      >
        {
          Array.from(
            new Array(numPages),
            (el, index) => (
              <Page
                key={`page_${index + 1}`}
                pageNumber={index + 1}
              />
            ),
          )
        }
      </Document>
      {!!download && <Button title="Download" onClick={handleDownload} />}
    </div>
  )
}

export default ReportReader;
