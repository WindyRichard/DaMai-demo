def generate_response(**kwargs):
    """生成包含status和message的响应字典，并可以添加其他字段"""
    response = {
    }

    for key, value in kwargs.items():
        response[key] = value

    return response
