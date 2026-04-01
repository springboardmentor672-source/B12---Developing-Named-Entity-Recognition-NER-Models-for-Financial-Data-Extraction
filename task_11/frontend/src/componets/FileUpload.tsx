import { useCallback } from "react";
import { useDropzone } from "react-dropzone";

type Props = {
  onFileSelect: (file: File) => void;
};

const FileUpload = ({ onFileSelect }: Props) => {
  const onDrop = useCallback((acceptedFiles: File[]) => {
    if (acceptedFiles.length > 0) {
      onFileSelect(acceptedFiles[0]);
    }
  }, [onFileSelect]);

  const { getRootProps, getInputProps } = useDropzone({
    onDrop,
  } as any);

  return (
    <div
      {...getRootProps()}
      style={{
        border: "2px dashed gray",
        padding: "30px",
        textAlign: "center",
        cursor: "pointer",
      }}
    >
      <input {...(getInputProps() as any)} />
      <p>📄 Upload PDF (Drag & Drop)</p>
    </div>
  );
};

export default FileUpload;