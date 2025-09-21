import axiosInstance from "../../util/axios";
import { useEffect } from "react";

const FileUpload = () => {
  useEffect(() => {
    axiosInstance.get("/files/list").then((res) => {
      console.log("response", res.data);
    });
  }, []);

  //폼 업로드 버튼 클릭 함수
  const handleSubmit = (e) => {
    e.preventDefault();
    const file = e.target.file.files[0];

    // 파일 선택 검증
    if (!file) {
      alert("파일을 선택해주세요.");
      return;
    }

    const formData = new FormData();
    formData.append("file", file);

    //파일 업로드 요청
    axiosInstance
      .post("/upload", formData)
      .then((res) => {
        console.log("response", res);
        alert("파일 업로드 성공!");
      })
      .catch((err) => {
        //console.log("error", err);
        alert("파일 업로드 실패: " + err.message);
      });
  };

  return (
    <form onSubmit={handleSubmit}>
      <input type="file" name="file" />
      <button type="submit">Upload</button>
    </form>
  );
};

export default FileUpload;
