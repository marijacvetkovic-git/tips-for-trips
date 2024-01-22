import { useState,useEffect } from "react";
import { useLocation } from "react-router-dom";
import axios from "axios";
import { Image, List } from "antd";
import { Carousel } from "antd";
import { Button, Modal, Space,Popover,Col,Row,Rate } from "antd";
import { CheckCircleTwoTone, QuestionCircleTwoTone } from "@ant-design/icons";
import { getUserId } from "../utils";

const Attraction = () => {
  const location = useLocation();
  const attractionId = location.state;
  const [attractionName, setAttractionName] = useState("");
  const [attractionDescription, setAttractionDescription] = useState("");
  const [attractionActivities, setAttractionActivities] = useState([]);
  const [attractionRelationship, setAttractionRelationship] = useState([]);
  const [attractionHashtags, setAttractionHashtags] = useState([]);
  const [attractionImages,setAttractionImages]=useState([])
  const [attractionAvgRate,setAttractionAvgRate]=useState(5)
  const [isModalOpen, setIsModalOpen] = useState(false);
  const [modalContent, setModalContent] = useState("");
  const [modalTitle, setModalTitle] = useState("");
  const [visited,setVisited]=useState(false)
  const [rateValue,setRateValue]=useState(0)
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
  const getData=()=>{
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
          setAttractionImages(responce.data[0]["images"]);
          setAttractionAvgRate(responce.data[0]["avgRate"]);
          console.log(responce.data[0]["images"]);
        }
      })
      .catch((error) => {
        console.error("Error:", error);
      });
  }
  useEffect(() => {getData()},[]);
  const [open, setOpen] = useState(false);
  const hide = () => {
    console.log("Hide")
    setOpen(false);
  };
  const done = () => {
    console.log(rateValue);
    console.log("Done");
    const idOfAttraction=attractionId
    const idOfUser=getUserId()
    const rate=rateValue
    const body = {
      idOfAttraction,
      idOfUser,
      rate,
    };
    axios
      .post(`http://127.0.0.1:5000/user/createRelationship_VISITED`, body, {
        headers: {
          Authorization: `Bearer ${localStorage.getItem("token")}`,
        },
      })
      .then((responce) => {
        if (responce.status === 200) {
          setVisited(true)
          setOpen(false)
          getData()
        }
      })
      .catch((error) => {
        console.error("Error:", error);
      });
    

  };
  const handleOpenChange = (newOpen) => {
    console.log("onChange")
    console.log(newOpen)

    setOpen(newOpen);
  };
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

useEffect(()=>{
  if(localStorage.getItem("token")){
  axios
    .get(`http://127.0.0.1:5000/user/isVisited/${attractionId}/${getUserId()}`, {
      headers: {
        Authorization: `Bearer ${localStorage.getItem("token")}`,
      },
    })
    .then((responce) => {
      if (responce.status === 200) {
        console.log(responce.data);
        setVisited(responce.data);
      }
    })
    .catch((error) => {
      console.error("Error:", error);
    });

  }
},[visited])


const rateContent = (
  <Rate value={rateValue} onChange={(value) => setRateValue(value)} />
);
  return (
    <>
      <div
        style={{
          // display: "flex",
          alignItems: "center",
          justifyContent: "center",
        }}
      >
        <div
          style={{
            display: "flex",
            justifyContent: "center",
            marginBottom: "10px",
            textAlign: "center",
            flex: 1,
          }}
        >
          <h1 style={{ margin: 0 }}>{attractionName}</h1>
        </div>

        <div style={{ display: "flex", justifyContent: "end"}}>
          {localStorage.getItem("token") &&
            (visited ? (
              <>
                <CheckCircleTwoTone
                  label="Visited"
                  twoToneColor="#52c41a"
                  style={{ fontSize: "24px", marginRight: "5px" }}
                />
                <span style={{ color: "#52c41a" }}>Visited</span>
              </>
            ) : (
              <>
                <Popover
                  content={
                    <div>
                      {rateContent}
                      <div>
                        <a onClick={hide}>Close</a>
                      </div>
                      <div>
                        {" "}
                        <a onClick={done}>Rate</a>
                      </div>
                    </div>
                  }
                  title="Rate visited attraction"
                  trigger="click"
                  open={open}
                  onOpenChange={handleOpenChange}
                >
                  <a style={{ color: "#C44C37" }}>
                    <QuestionCircleTwoTone
                      twoToneColor="#C44C37"
                      style={{ fontSize: "24px", marginRight: "5px" }}
                    />
                    Not visited yet
                  </a>
                </Popover>
                {/* <a
                  href="#"
                  onClick={(e) => {
                    e.preventDefault(); // Ovo sprečava defaultno ponašanje linka (npr. da se preusmeri na drugu stranicu)
                    handleNotVisitedClick();
                  }}
                  style={{
                    display: "flex",
                    alignItems: "center",
                    textDecoration: "underline",
                    color: "#C44C37",
                  }}
                >
                  <Popover
                    content={<a onClick={hide}>Close</a>}
                    title="Title"
                    trigger="click"
                    open={open}
                    onOpenChange={handleNotVisitedClick}
                  >
                    <span>
                      <QuestionCircleTwoTone
                        twoToneColor="#C44C37"
                        style={{ fontSize: "24px", marginRight: "5px" }}
                      />
                      Not visited yet
                    </span>
                  </Popover>
                </a> */}
              </>
            ))}
        </div>
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
      <>
        <Rate disabled value={attractionAvgRate}  />
        <span>{attractionAvgRate.toFixed(2)}</span>
      </>
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
