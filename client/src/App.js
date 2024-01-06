
import './App.css';
import {BrowserRouter as Router,Routes,Route,Link} from "react-router-dom"
import MenuItem from "antd/es/menu/MenuItem";
import axios from 'axios';
import Register from './components/Register'
import Home from './components/Home'
import LogIn from './components/LogIn';
import Attraction from './components/Attraction'
import {useState} from 'react'
import React from 'react';
import { Layout, Menu, theme,Input } from 'antd';
import { getExpiration, getUsername } from './utils';
import {
  LoginOutlined,
  CrownOutlined,
  HomeOutlined,
  HeartOutlined,
} from "@ant-design/icons"; 
import Preferences from './components/Preferences';
const { Search } = Input;


const { Header, Content, Footer } = Layout;
function App() {
const handleOnSearch=(value, _e, info) => {
      console.log(value)
      axios.get(`http://127.0.0.1:5000/user/searchEngineNotLoggedIn/${value}`)
      .then(responce=>{
        if(responce.status===200)
        {
          console.log(responce.data)
        }
      })
      };
const {
    token: { colorBgContainer, borderRadiusLG },
  } = theme.useToken();
  const logOut=()=>{
    localStorage.removeItem("token");
    window.location = "/";
  }
  const isTokenExpired = () => {
    let exp=getExpiration()
    exp = exp * 1000;
    const currentTime = new Date().getTime();
  if(currentTime >= exp)
  {
    localStorage.removeItem("token");
    window.location = "/";
  }

  };
  useState(()=>{
    isTokenExpired()
  })


  const username = getUsername();

  return (
    <Router>
      <Layout style={{minHeight:"100vh"}}>
      <Header
        style={{
          display: 'flex',
          alignItems: 'center',
        }}
      >
        <div className="demo-logo" />
    <Menu
          theme="dark"
          mode="horizontal"
          defaultSelectedKeys={"1"}
          style={{
            flex: 1,
            minWidth: 0,
          }}
        > 
        <MenuItem
        key={"1"}
        style={{float:"left"}}
        >
        <Link to={"/home"}>Home</Link>
        </MenuItem>
        {!(localStorage.getItem("token")) ? (
        <MenuItem
        key={"2"}
        style={{float:"left"}}
        >
          <Link to={"/register"}>Register/LogIn</Link>
        </MenuItem>
        ):(

         <MenuItem
        key={"2"}
        style={{float:"left"}}
        >
        <Link onClick={logOut}>LogOut</Link>
        </MenuItem>
        )
}
 <MenuItem
        key={"3"}
        style={{alignSelf:"right"}}
        >
        <Search style={{marginTop:"20px"}} placeholder="Input search text" onSearch={handleOnSearch} enterButton />
        </MenuItem>
        </Menu>
      </Header>
      <Content
        style={{
          padding: '48px 48px',
        }}
      >
        <div
          style={{
            background: colorBgContainer,
            minHeight: 280,
            padding: 24,
            borderRadius: borderRadiusLG,
          }}
        >

         <Routes>
              <Route path="/" element={<Home />} />
              <Route path="/home" element={<Home />} />
              <Route path="/register" element={<Register />} />
              <Route path="/preferences" element={<Preferences />} />
              <Route path="/login" element={<LogIn/>}/>
              <Route path="/attraction" element={<Attraction/>}/>
         </Routes>
        </div>

      </Content>
      <Footer
        style={{
          textAlign: 'center',
        }}
      >
        TipsForTrips ©{new Date().getFullYear()} 
      </Footer>
    </Layout>
    </Router>
  );
}

export default App;
