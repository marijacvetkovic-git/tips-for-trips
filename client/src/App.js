
import './App.css';
import {BrowserRouter as Router,Routes,Route,Link} from "react-router-dom"
import MenuItem from "antd/es/menu/MenuItem";

import Register from './components/Register'
import Homes from './components/Homes'
import LogIn from './components/LogIn';
import {useState} from 'react'
import React from 'react';
import { Breadcrumb, Layout, Menu, theme } from 'antd';
import { getUsername } from './utils';
import {
  LoginOutlined,
  CrownOutlined,
  HomeOutlined,
  HeartOutlined,
} from "@ant-design/icons"; 
import Preferences from './components/Preferences';

const { Header, Content, Footer } = Layout;
function App() {
const {
    token: { colorBgContainer, borderRadiusLG },
  } = theme.useToken();
  const logout = () => {
    localStorage.removeItem("token");
    window.location = "/";
  };
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
        <MenuItem
        key={"2"}
        style={{float:"left"}}
        >
          <Link to={"/register"}>Register</Link>
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
              <Route path="/" element={<Homes />} />
              <Route path="/home" element={<Homes />} />
              <Route path="/register" element={<Register />} />
              <Route path="/preferences" element={<Preferences />} />
              <Route path="/login" element={<LogIn/>}/>
         </Routes>
        </div>

      </Content>
      <Footer
        style={{
          textAlign: 'center',
        }}
      >
        Ant Design ©{new Date().getFullYear()} Created by Ant UED
      </Footer>
    </Layout>
    </Router>
  );
}

export default App;
