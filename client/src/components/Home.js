import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import axios from "axios";
import { getUserId } from "../utils";
import { Card, Space, Input, FloatButton, Switch } from "antd";
import { EnvironmentOutlined, CloseCircleOutlined } from "@ant-design/icons";

const { Meta } = Card;
const { Search } = Input;
const cardStyle = {
  width: 620,
};
const imgStyle = {
  display: "block",
  width: 273,
};

const Home = () => {
  const navigate = useNavigate();
  const [nearYou, setNearYou] = useState(false);
  const [listOfAttractions, setListOfAttractions] = useState([]);
  const [listMostRecommendeLogIn,setListMostRecommendeLogIn]=useState([]);
  const [title, setTitle] = useState("Recommended for you");
  useEffect(() => {
    console.log(localStorage.getItem("token"));
    if (localStorage.getItem("token") === null) {
      axios
        .get("http://127.0.0.1:5000/helpers/returnMostRecommendedAttractions")
        .then((responce) => {
          if (responce.status === 200) {
            setTitle("Most recommended");

            console.log(responce.data["listOfAttractions"]);
            setListOfAttractions(responce.data["listOfAttractions"]);
          }
        })
        .catch((error) => {
          console.error("Error:", error);
        });
    } else {
      const userId = getUserId();
      console.log(userId);
      console.log(localStorage.getItem("token"));
      if (nearYou == false) {
        axios
          .get(`http://127.0.0.1:5000/user/recommend/${userId}`, {
            headers: {
              Authorization: `Bearer ${localStorage.getItem("token")}`,
            },
          })
          .then((responce) => {
            if (responce.status === 200) {
              console.log(responce.data);
              setTitle("Recommended for you ");

              // console.log(responce.data["listOfAttractions"])
              setListOfAttractions(responce.data);
            }
          })
          .catch((error) => {
            console.error("Error:", error);
          });
      } else {
        axios
          .get(`http://127.0.0.1:5000/user/nearYouRecommendation/${userId}`, {
            headers: {
              Authorization: `Bearer ${localStorage.getItem("token")}`,
            },
          })
          .then((responce) => {
            if (responce.status === 200) {
              console.log(responce.data);
              setListOfAttractions(responce.data);
              setTitle("Near you");
            }
          })
          .catch((error) => {
            console.error("Error:", error);
          });
      }

      axios
        .get("http://127.0.0.1:5000/helpers/returnMostRecommendedAttractions")
        .then((responce) => {
          if (responce.status === 200) {
            console.log(responce.data["listOfAttractions"]);
            setListMostRecommendeLogIn(responce.data["listOfAttractions"]);
          }
        })
        .catch((error) => {
          console.error("Error:", error);
        });
    }
  }, [nearYou]);

  const handleOnClick = (id) => {
    console.log(id);
    navigate("/attraction", { state: id });
  };
  const handleOnSearch = (value, _e) => {
    console.log(value);
    navigate("/search", { state: value });
  };
  const spaceStyle = {
    display: "flex",
    flexWrap: "wrap",
    justifyContent: "space-between", // Možete eksperimentisati sa ovim vrednostima
  };

  return (
    <>
      <Search
        style={{ marginBottom: "50px" }}
        placeholder="Search"
        onSearch={handleOnSearch}
        enterButton
      />
      <div style={{ textAlign: "center", marginTop: "20px" }}>
        <h1
          style={{
            fontFamily: "'Playfair Display', serif",
            fontWeight: 550,
            fontSize: "50px",
            margin: "10px 0",
            fontStyle: "italic",
          }}
        >
          Welcome to TipsForTrips
        </h1>
        <img
          src="/logo.png"
          alt="TipsForTrips Logo"
          style={{ marginBottom: "10vh", width: "17vw", height: "auto" }}
        />
      </div>

      <h1
        style={{
          fontFamily: "'Playfair Display', serif",

          fontWeight: 600,
          color: "#133115",
          fontSize: "22px",
          margin: "10px 0",
        }}
      >
        {title}
      </h1>

      <Space size={[8, 16]} style={spaceStyle} wrap>
        {listOfAttractions &&
          listOfAttractions.map((item) => (
            <Card
              hoverable
              value={item["id"]}
              id={item["id"]}
              style={{
                width: 240,
              }}
              onClick={() => handleOnClick(item["id"])}
              cover={
                <img
                  alt="example"
                  src={item["image"]}
                  style={{
                    display: "block",
                    width: "100%",
                    height: "30vh",
                  }}
                />
              }
            >
              <Meta title={item["name"]} />
            </Card>
          ))}
      </Space>
      {localStorage.getItem("token") && (
        <>
          <h1
            style={{
              fontFamily: "'Playfair Display', serif",

              fontWeight: 600,
              color: "#133115",
              fontSize: "22px",
              margin: "10px 0",
              marginTop: "7vh",
            }}
          >
            Most Recommended
          </h1>

          <Space size={[8, 16]} style={spaceStyle} wrap>
            {listMostRecommendeLogIn &&
              listMostRecommendeLogIn.map((item) => (
                <Card
                  hoverable
                  value={item["id"]}
                  id={item["id"]}
                  style={{
                    width: 240,
                  }}
                  onClick={() => handleOnClick(item["id"])}
                  cover={
                    <img
                      alt="example"
                      src={item["image"]}
                      style={{
                        display: "block",
                        width: "100%",
                        height: "30vh",
                      }}
                    />
                  }
                >
                  <Meta title={item["name"]} />
                </Card>
              ))}
          </Space>
        </>
      )}

      {localStorage.getItem("token") &&
        (nearYou == false ? (
          <FloatButton
            icon={<EnvironmentOutlined />}
            type="primary"
            style={{
              right: 24,
              fontSize: "36px", // Adjust the fontSize as needed
              width: "50px", // Adjust the width as needed
              height: "50px", // Adjust the height as needed
              // Add any other styling properties you want to customize
            }}
            title="Near you"
            onClick={() => setNearYou(true)}
          />
        ) : (
          <FloatButton
            icon={<CloseCircleOutlined />}
            type="primary"
            style={{
              right: 24,
              fontSize: "36px", // Adjust the fontSize as needed
              width: "50px", // Adjust the width as needed
              height: "50px", // Adjust the height as needed
              // Add any other styling properties you want to customize
            }}
            title="Recommended for you"
            onClick={() => setNearYou(false)}
          />
        ))}
    </>
  );
};
export default Home;
