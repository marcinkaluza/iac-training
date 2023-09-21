import React from "react";
import "./Comment.css";

function Comment({ comment }) {
  return (
    <div className="comment">
      <strong>{comment.author}</strong>
      <p>{comment.text}</p>
    </div>
  );
}

export default Comment;
