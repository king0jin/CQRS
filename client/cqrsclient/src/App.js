import React, {useEffect, useState} from 'react';
import './App.css';
import {Paper} from "@material-ui/core"
import PostBook from "./PostBook";
import Axios from "axios";

function App() {
  //상태를 생성 -> 변수, 접근자 함수 생성
  const [items, setItems] = useState([]);
  //데이터 동기화를 하기위한 상태 생성
  const [data, setData] = useState(0);
  const [error, setError] = useState("");

  //화면이 출력되자마자 수행될 함수 : 데이터 가져오기 (MongoDB 기준)
  useEffect(() => {
    console.log("렌더링 후 바로 수행 : componentDidMount()");
    Axios.get("http://127.0.0.1:7000/cqrs/books/").then((response) => {
      //console.log(response.data)
      if (response.data) {
        setItems(response.data)
      } else {
        setError("Failed Read");
      }
    }).catch(() => setError("서버와 통신 중 문제가 발생했습니다.1"));
  }, [data]); //data가 변경된 경우에 동작

   //데이터 추가를 위한 함수
   const post = (book) => {
    console.log("book : ", book);
      Axios.post("http://127.0.0.1:8080/cqrs/book/", book).then((response) => {
        console.log(response.data)
        if (response.data.bid) {
          alert("정보를 저장하는데 성공했습니다.")
          //데이터 추가 성공시, 상태를 변경해서 화면 재출력 
          setData(1)
        } else {
          alert("정보를 저장하는데 실패했습니다.");
        }
      }).catch(() => setError("서버와 통신 중 문제가 발생했습니다.2"));
    };

  return (
    <div className="App">
      {error && <div style={{ color: "red" }}>{error}</div>}
      <Paper style={{ margin: 16 }}>
        <PostBook post = {post}/>
      </Paper> 
      {items.map((item) => (
        <p key = {item.bid}>
          {item.title}
        </p>
      ))}   
    </div>
  );
}

export default App;
