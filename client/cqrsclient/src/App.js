import React, {useEffect, useState} from 'react';
import './App.css';
import {Paper} from "@material-ui/core"
import PostBook from "./PostBook";
import Axios from "axios";

function App() {
  //상태를 생성 -> 변수, 접근자 함수 생성
  const [items, setItems] = useState([]);

  //화면이 출력되자마자 수행될 함수
  useEffect(() => {
    console.log("렌더링 후 바로 수행 : componentDidMount()");
    Axios.get("http://127.0.0.1:8000/cqrs/books/").then((response) => {
      //console.log(response.data)
      if (response.data) {
        setItems(response.data)
      } else {
        alert("Failed Read");
      }
    });
  }, []);

   //데이터 추가를 위한 함수
   const post = (book) => {
    console.log("book : ", book);
      Axios.post("http://127.0.0.1:8080/cqrs/book/", book).then((response) => {
        console.log(response.data)
        if (response.data.bid) {
          alert("정보를 저장하는데 성공했습니다.")
        } else {
          alert("정보를 저장하는데 실패했습니다.");
        }
      });
    };

  return (
    <div className="App">
       <Paper style={{ margin: 16 }}>
        <PostBook post = {post}/>
      </Paper> 
      {items.map((item, index) => (
        <p key = {index}>
          {item.title}
        </p>
      ))}   
    </div>
  );
}

export default App;
