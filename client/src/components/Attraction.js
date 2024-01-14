import { useState,useEffect } from "react";
import { useLocation } from "react-router-dom";
import axios from "axios";
import { Image, List } from "antd";
import { Carousel } from "antd";
import { Button, Modal, Space } from "antd";
import { Col, Divider, Row } from "antd";

const Attraction = () => {
  const location = useLocation();
  const attractionId = location.state;
  const [attractionName, setAttractionName] = useState("");
  const [attractionDescription, setAttractionDescription] = useState("");
  const [attractionActivities, setAttractionActivities] = useState([]);
  const [attractionRelationship, setAttractionRelationship] = useState([]);
  const [attractionHashtags, setAttractionHashtags] = useState([]);
  const [attractionImages,setAttractionImages]=useState([])
  const [isModalOpen, setIsModalOpen] = useState(false);
  const [modalContent, setModalContent] = useState("");
  const [modalTitle, setModalTitle] = useState("");
  const showModal = (item, content) => {
    console.log(content);
    let experience = "not needed";
    if (content.experience == true) experience = "needed";

    setModalContent(
      <>
        Duration of activity: {content.durationOfActivity}
        <br />
        Experience: {experience}
        <br />
        Age limit between {content.minAge}-{content.maxAge}
      </>
    );
    setModalTitle(item);
    setIsModalOpen(true);
  };
  const handleOk = () => {
    setIsModalOpen(false);
  };
  // const onHashtag=()=>{}
  useEffect(() => {
    console.log(localStorage.getItem("token"));
    console.log(attractionId);
    axios
      .get(`http://127.0.0.1:5000/helpers/returnAttraction/${attractionId}`)
      .then((responce) => {
        if (responce.status === 200) {
          console.log(responce.data);
          setAttractionName(responce.data[0]["name"]);
          setAttractionDescription(responce.data[0]["description"]);
          setAttractionActivities(responce.data[0]["activities"]);
          setAttractionRelationship(responce.data[0]["relationship"]);
          setAttractionHashtags(responce.data[0]["hashtags"]);
          setAttractionImages(responce.data[0]["images"])
          console.log(responce.data[0]["images"]);
        }
      })
      .catch((error) => {
        console.error("Error:", error);
      });
  }, []);
   const [currentSlide, setCurrentSlide] = useState(0);


const nextSlide = () => {
  setCurrentSlide((prevSlide) => (prevSlide + 1) % attractionImages.length);
};

const prevSlide = () => {
  setCurrentSlide(
    (prevSlide) => (prevSlide - 1 + attractionImages.length) % attractionImages.length
  );
};

const carouselStyle = {
  width: "60%", // Podesite željenu širinu karusela
  margin: "auto", // Centrirajte karusel na stranici
  overflow: "hidden",
};

const slideContainerStyle = {
  display: "flex",
  width: `${attractionImages.length * 100}%`,
  transform: `translateX(-${currentSlide * (100 / attractionImages.length)}%)`,
  transition: "transform 0.5s",
};

const imageStyle = {
  width: `${100 / attractionImages.length}%`,
  height: "95vh",
  flex: "0 0 auto",
};
  return (
    <>
      <div>
        <h1 style={{ textAlign: "center" }}>{attractionName}</h1>
      </div>
      <div style={carouselStyle}>
        <div style={slideContainerStyle}>
          {attractionImages.map((imageUrl, index) => (
            <img
              key={index}
              src={imageUrl}
              alt={`Slide ${index + 1}`}
              style={imageStyle}
            />
          ))}
        </div>
        <div
          style={{
            display: "flex",
            justifyContent: "center",
            marginTop: "10px",
          }}
        >
          {attractionImages.map((_, index) => (
            <div
              key={index}
              onClick={() => setCurrentSlide(index)}
              style={{
                width: "10px",
                height: "10px",
                borderRadius: "50%",
                background: currentSlide === index ? "black" : "gray",
                margin: "0 5px",
                cursor: "pointer",
              }}
            ></div>
          ))}
        </div>
      </div>

      <div>
        <h2>
          <i>Fun facts:</i>
        </h2>
        <p>{attractionDescription}</p>

        {attractionActivities.length != 0 && (
          <>
            <h2>
              <i>Activities:</i>
            </h2>
            <Space>
              {
                <List
                  bordered
                  dataSource={attractionActivities}
                  renderItem={(item, index) => (
                    <List.Item>
                      <a
                        key={item}
                        onClick={() =>
                          showModal(item, attractionRelationship[index])
                        }
                        style={{ cursor: "pointer" }}
                      >
                        {item}
                      </a>
                    </List.Item>
                  )}
                />
              }
            </Space>
          </>
        )}

        <Row
          gutter={{
            xs: 8,
            sm: 16,
            md: 24,
            lg: 32,
          }}
          style={{ marginTop: "10px" }}
        >
          {attractionHashtags.map((item) => (
            <Col>
              <a key={item} style={{ cursor: "pointer" }}>
                #{item}
              </a>
            </Col>
          ))}
        </Row>
        <Modal
          onOk={handleOk}
          footer={[
            <Button key="ok" onClick={handleOk}>
              Ok
            </Button>,
          ]}
          closable={false}
          open={isModalOpen}
          title={modalTitle}
        >
          <p>{modalContent}</p>
        </Modal>
      </div>
    </>
  );
};
export default Attraction;
