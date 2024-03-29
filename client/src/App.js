
import './App.css';
import {BrowserRouter as Router,Routes,Route,Link} from "react-router-dom"
import MenuItem from "antd/es/menu/MenuItem";
import Register from './components/Register'
import Home from './components/Home'
import LogIn from './components/LogIn';
import Attraction from './components/Attraction'
import SearchAttractions from './components/SearchAttractions';
import PlanYourTrip from './components/PlanYourTrip';
import Profile from './components/Profile';
import Admin from './components/Admin';
import {useState} from 'react'
import React from 'react';
import { Layout, Menu, theme } from 'antd';
import { getExpiration, getUserRole, getUsername } from './utils';
import { UserOutlined } from "@ant-design/icons";
import { Avatar } from "antd";



import Preferences from './components/Preferences';

const { Header, Content, Footer } = Layout;

function App() {
  const username=getUsername();
  const [seeSearch,setSeeSearch]=useState(true)


  const {
    token: { colorBgContainer, borderRadiusLG },
  } = theme.useToken();

  const logOut=()=>{
    localStorage.removeItem("token");
    window.location = "/home";
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



  return (
    <Router>
      <Layout style={{ minHeight: "100vh" }}>
        <Header
          style={{
            display: "flex",
            alignItems: "center",
            backgroundColor: "#294B29",
          }}
        >
          <div className="demo-logo" />
          <Menu
            theme="dark"
            mode="horizontal"
            defaultSelectedKeys={"1"}
            style={{
              backgroundColor: "#294B29",

              flex: 1,
              minWidth: 0,
            }}
          >
            {localStorage.getItem("token") && (
              <MenuItem key={"0"} style={{ float: "left" }}>
                <Avatar
                  style={{
                    backgroundColor: "#87d068",
                  }}
                  icon={<UserOutlined />}
                />
                <Link to={"/profile"}></Link>
              </MenuItem>
            )}
            <MenuItem key={"1"} style={{ float: "left" }}>
              <Link to={"/home"}>Home</Link>
            </MenuItem>
            {!localStorage.getItem("token") ? (
              <MenuItem key={"2"} style={{ float: "left" }}>
                <Link to={"/register"}>Register/LogIn</Link>
              </MenuItem>
            ) : (
              <>
                <MenuItem key={"2"} style={{ float: "left" }}>
                  <Link to={"/planYourTrip"}>Plan trip</Link>
                </MenuItem>

                {getUserRole() == true && (
                  <MenuItem key={"3"} style={{ float: "left" }}>
                    <Link to={"/admin"}>Admin</Link>
                  </MenuItem>
                )}
                <MenuItem key={"4"} style={{ float: "left" }}>
                  <Link onClick={logOut}>Log Out</Link>
                </MenuItem>
              </>
            )}
          </Menu>
        </Header>
        <Content
          style={{
            padding: "48px 48px",
            background: "#DBE7C9",
          }}
        >
          <div
            style={{
              background: "white",
              minHeight: 280,
              padding: 24,

              borderRadius: borderRadiusLG,
            }}
          >
            {/* <div
            style={{
              background: colorBgContainer,
              backgroundColor:"#89BA90",
              minHeight: 280,
              padding: 24,
              borderRadius: borderRadiusLG,
            }}
          > */}
            <Routes>
              <Route path="/" element={<Home />} />
              <Route path="/home" element={<Home />} />
              <Route path="/register" element={<Register />} />
              <Route path="/preferences" element={<Preferences />} />
              <Route path="/login" element={<LogIn />} />
              <Route path="/attraction" element={<Attraction />} />
              <Route path="/search" element={<SearchAttractions />} />
              <Route path="/planYourTrip" element={<PlanYourTrip />} />
              <Route path="/profile" element={<Profile />} />
              <Route path="/admin" element={<Admin />} />
            </Routes>
          </div>
        </Content>
        <Footer
          style={{
            textAlign: "center",
          }}
        >
          TipsForTrips ©{new Date().getFullYear()}
        </Footer>
      </Layout>
    </Router>
  );
}

export default App;
