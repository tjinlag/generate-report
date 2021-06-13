import React, { useState } from 'react';
import { Document, Page } from 'react-pdf/dist/esm/entry.webpack';
import Button from '../../../components/Button';

const options = {
  cMapUrl: 'cmaps/',
  cMapPacked: true,
};

type IProps = {
  title?: string;
  data: null | {
    report: string;
    excel_file: string;
  };
  download?: boolean;
}

const ReportReader = ({title, data, download = false} : IProps) => {
  const [numPages, setNumPages] = useState(null);

  const onDocumentLoadSuccess = ({ numPages: nextNumPages } : any) => {
    setNumPages(nextNumPages);
  }

  const handleDownload = (fileName: string) => () => {
    window.open(fileName);
  }

  if (!data) return null;

  return (
    <div className="pdf-container">
      {!!title && <h1>{title}</h1>}
      <Document
        file={data.report}
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
      {!!download && <Button title="Download Report" onClick={handleDownload(data.report)} />}
      {!!download && <Button title="Download Excel File" onClick={handleDownload(data.excel_file)} />}
    </div>
  )
}

export default ReportReader;
