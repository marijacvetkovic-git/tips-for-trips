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
  const [title, setTitle] = useState("Recommended for U <3");
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
              setTitle("Recommended for U <3");

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
              setTitle("Near U");
            }
          })
          .catch((error) => {
            console.error("Error:", error);
          });
      }
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

  return (
    <>
      <Search
        style={{ marginBottom: "50px" }}
        placeholder="Search"
        onSearch={handleOnSearch}
        enterButton
      />
      <h1>{title}</h1>
      <Space size={[8, 16]} wrap>
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
                  src="https://os.alipayobjects.com/rmsportal/QBnOOoLaAfKPirc.png"
                />
              }
            >
              <Meta title={item["name"]} />
            </Card>
          ))}
      </Space>
      {localStorage.getItem("token") &&
        (nearYou == false ? (
          <FloatButton
            icon={<EnvironmentOutlined />}
            type="primary"
            style={{
              right: 24,
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
            }}
            title="Recommended for you"
            onClick={() => setNearYou(false)}
          />
        ))}
    </>
  );
};
export default Home;
