import logo from './logo.svg';
import './App.css';
import {Paper} from "@material-ui/core"
import PostBook from "./PostBook";
import Axios from "axios";


function App() {
   //데이터 추가를 위한 함수
   const post = (book) => {
    console.log("book : ", book);
      Axios.post("http://127.0.0.1:8080/cqrs/book/", book).then((response) => {
        console.log(response.data)
        if (response.data.bid) {
          alert("저장에 성공했습니다.")
        } else {
          alert("코멘트를 저장하지 못했습니다.");
        }
      });
    };

  return (
    <div className="App">
       <Paper style={{ margin: 16 }}>
        <PostBook post = {post}/>
      </Paper> 
    </div>
  );
}

export default App;
