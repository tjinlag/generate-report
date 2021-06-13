import React from 'react';
import Button from '../../../components/Button';

type IProps = {
  onClick: () => void;
}

const ReportButton = ({ onClick} : IProps) => (
  <Button title="Show Report" onClick={onClick} />
)

export default ReportButton;
