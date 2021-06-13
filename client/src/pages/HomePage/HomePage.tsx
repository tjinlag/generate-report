import React, { useState } from 'react';
import ReportReader from './components/ReportReader';
import { getReportAssets } from '../../services/report';
import Loading from '../../components/Loading';
import ReportButton from './components/ReportButton';

const HomePage = () => {
  const [loading, setLoading] = useState(false);
  const [report, setReport] = useState(null);

  const handleReportShow = async () => {
    setLoading(true);
    const {ok, data} = await getReportAssets();
    setLoading(false);
    if (!ok || !data.report) {
      alert("Have error when generate report")
      return;
    }
    setReport(data.report);
  }

  return (
    <div className="container">
      {!!loading && <Loading />}
      {!report
        ? <ReportButton onClick={handleReportShow} />
        : <ReportReader file={report} title="The Report" download />}
    </div>
  );
}

export default HomePage;
