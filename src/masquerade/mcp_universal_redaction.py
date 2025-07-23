from mcp.server.fastmcp import FastMCP
import os
import subprocess
from masquerade.redact_content import redact_content, get_supported_formats
from masquerade.tinfoil_llm import TinfoilLLM

# Create a FastMCP server instance
mcp = FastMCP(name="UniversalRedactionServer")
tinfoil_llm = TinfoilLLM()

@mcp.tool("redact_content")
def process_content(params):
    """
    Universal redaction tool that handles PDFs, code files, and text content.
    
    Parameters can be:
    - String: file path or text content
    - Dict: with keys like 'file_path', 'text', 'content_type', etc.
    """
    try:
        # Process the input
        result = redact_content(params, tinfoil_llm)
        
        if result.get("success"):
            # Try to open files if they exist
            if result.get("content_type") == "pdf":
                try:
                    redacted_path = result["redaction_summary"]["redacted_pdf_path"]
                    highlighted_path = result["highlighted_path"]
                    
                    # Try to open files
                    try:
                        subprocess.run(["open", redacted_path], check=True)
                        subprocess.run(["open", highlighted_path], check=True)
                    except subprocess.CalledProcessError:
                        try:
                            subprocess.run(["xdg-open", redacted_path], check=True)
                            subprocess.run(["xdg-open", highlighted_path], check=True)
                        except (subprocess.CalledProcessError, FileNotFoundError):
                            print(f"Warning: Could not open PDF files automatically")
                except Exception as e:
                    print(f"Warning: Could not open files: {e}")
            
            elif result.get("content_type") == "code":
                try:
                    redacted_path = result["redaction_result"]["redacted_file_path"]
                    try:
                        subprocess.run(["open", redacted_path], check=True)
                    except subprocess.CalledProcessError:
                        try:
                            subprocess.run(["xdg-open", redacted_path], check=True)
                        except (subprocess.CalledProcessError, FileNotFoundError):
                            print(f"Warning: Could not open code file automatically")
                except Exception as e:
                    print(f"Warning: Could not open file: {e}")
        
        return result
        
    except Exception as e:
        return {"success": False, "error": f"Error processing content: {str(e)}"}

@mcp.tool("redact_pdf")
def process_pdf(params):
    """
    Legacy PDF redaction tool for backward compatibility.
    """
    return process_content(params)

@mcp.tool("redact_code")
def process_code(params):
    """
    Code file redaction tool.
    """
    if isinstance(params, str):
        params = {"file_path": params, "content_type": "code"}
    elif isinstance(params, dict):
        params["content_type"] = "code"
    
    return process_content(params)

@mcp.tool("redact_text")
def process_text(params):
    """
    Text content redaction tool.
    """
    if isinstance(params, str):
        params = {"text": params, "content_type": "text"}
    elif isinstance(params, dict):
        params["content_type"] = "text"
    
    return process_content(params)

@mcp.tool("get_supported_formats")
def get_formats(params=None):
    """
    Get list of supported file formats and content types.
    """
    return {
        "success": True,
        "supported_formats": get_supported_formats()
    }

# Define resources for different content types
@mcp.resource("content://redact")
def redact_content_endpoint():
    return {
        "meta": None,
        "contents": [{
            "uri": "content://redact",
            "mime_type": "application/json",
            "text": "Universal content redaction endpoint"
        }]
    }

@mcp.resource("pdf://redact")
def redact_pdf_endpoint():
    return {
        "meta": None,
        "contents": [{
            "uri": "pdf://redact",
            "mime_type": "application/json",
            "text": "PDF redaction endpoint"
        }]
    }

@mcp.resource("code://redact")
def redact_code_endpoint():
    return {
        "meta": None,
        "contents": [{
            "uri": "code://redact",
            "mime_type": "application/json",
            "text": "Code redaction endpoint"
        }]
    }

@mcp.resource("text://redact")
def redact_text_endpoint():
    return {
        "meta": None,
        "contents": [{
            "uri": "text://redact",
            "mime_type": "application/json",
            "text": "Text redaction endpoint"
        }]
    }

if __name__ == "__main__":
    mcp.run() 