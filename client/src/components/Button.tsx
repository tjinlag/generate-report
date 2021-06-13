import React from 'react';

type IProps = React.DetailedHTMLProps<React.ButtonHTMLAttributes<HTMLButtonElement>, HTMLButtonElement> & {
  title: string;
}

const Button = ({onClick, title, ...otherProps} : IProps) => {
  return (
    <div style={{ display: "flex", justifyContent: "center", marginTop: 10 }}>
      <button
        {...otherProps}
        type="button"
        className="btn"
        onClick={onClick}
      >{title}</button>
    </div>
  )
}

export default Button;
