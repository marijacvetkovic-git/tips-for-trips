import { useState } from "react";
import { useLocation } from "react-router-dom";
import axios from "axios";
import { Image, List } from "antd";
import { Carousel } from "antd";
import { Button, Modal, Space } from "antd";
import { Col, Divider, Row } from "antd";
const style = {
  background: "#0092ff",
  padding: "8px 0",
};

const Attraction = () => {
  const location = useLocation();
  const attractionId = location.state;
  const [attractionName, setAttractionName] = useState("");
  const [attractionDescription, setAttractionDescription] = useState("");
  const [attractionActivities, setAttractionActivities] = useState([]);
  const [attractionRelationship,setAttractionRelationship]=useState([]);
  const [attractionHashtags,setAttractionHashtags]=useState([]);

  const onChange = (currentSlide) => {
    console.log(currentSlide);
  };

  const contentStyle = {
    verticalAlign: "middle",
    // textAlign: "center",
    //         lineHeight: "100vh",
    width: "30vw",
    height: "50vh",
    backgroundColor: "green",
    marginLeft: "30vw",
    //   lineHeight: "160px",
    //   background: "#364d79",
  };
  const [isModalOpen, setIsModalOpen] = useState(false);
  const [modalContent, setModalContent] = useState("");
  const [modalTitle,setModalTitle]=useState("")
  const showModal = (item,content) => {
    console.log(content)
    let experience="not needed"
    if(content.experience==true)
        experience="needed"

    setModalContent(
      <>
        Duration of activity: {content.durationOfActivity}
        <br />
        Experience: {experience}
        <br />
        Age limit between {content.minAge}-{content.maxAge}
      </>
    );
    setModalTitle(item)
    setIsModalOpen(true);
  };
  const handleOk = () => {
    setIsModalOpen(false);
  };
// const onHashtag=()=>{}
  useState(() => {
    console.log(localStorage.getItem("token"));
    console.log(attractionId)
    axios
      .get(`http://127.0.0.1:5000/helpers/returnAttraction/${attractionId}`)
      .then((responce) => {
        if (responce.status === 200) {
          console.log(responce.data);
          setAttractionName(responce.data[0]["name"]);
          setAttractionDescription(responce.data[0]["description"]);
          setAttractionActivities(responce.data[0]["activities"]);
          setAttractionRelationship(responce.data[0]["relationship"]);
          setAttractionHashtags(responce.data[0]["hashtags"])
          console.log(responce.data[0]["hashtags"]);
        }
      });
  }, []);
  return (
    <>
      <div>
        <h1 style={{ textAlign: "center" }}>{attractionName}</h1>
      </div>
      <div>
        <Carousel style={{ justifyContent: "center" }} afterChange={onChange}>
          <div>
            <Image
              style={contentStyle}
              src="https://zos.alipayobjects.com/rmsportal/jkjgkEfvpUPVyRjUImniVslZfWPnJuuZ.png"
            />
          </div>
          <div>
            <Image
              style={contentStyle}
              src="https://zos.alipayobjects.com/rmsportal/jkjgkEfvpUPVyRjUImniVslZfWPnJuuZ.png"
            />
          </div>
          <div>
            <Image
              style={contentStyle}
              src="https://zos.alipayobjects.com/rmsportal/jkjgkEfvpUPVyRjUImniVslZfWPnJuuZ.png"
            />
          </div>
          <div>
            <Image
              style={contentStyle}
              src="https://zos.alipayobjects.com/rmsportal/jkjgkEfvpUPVyRjUImniVslZfWPnJuuZ.png"
            />
          </div>
        </Carousel>
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
          style={{marginTop:"10px"}}
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
