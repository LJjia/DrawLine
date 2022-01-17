
#include <stdio.h>
#include <stdlib.h>
#include <stdarg.h>

/*maigc head*/
#define YUV_FRAME_HEAD_MAGIC 0x7F800102
/*最大支持32个obj ,1个10顶点的多边形规则,*/
#define YUV_FRAME_MAX_OBJ_NUM 64
#define YUV_FRAME_MAX_ATTR_NUM 8
#define YUV_FRAME_MAX_RULE_NUM 1
#define YUV_FRAME_MAX_POINT_NUM 10
#define YUV_FRAME_MAX_LABEL_DESC 8
#define YUV_FRAME_INFO_FORMAT_JSON 1
#define YUV_FRAME_INFO_FORMAT_CSTRUCT 0

/*YUV数据头,存储在最后,与正常通信不同,由后向前存储*/
/*Len 32*/
typedef struct _YUV_FRAME_INFO_HEAD
{
    uint32_t magic;
    uint32_t datalen;
    uint32_t infoType;       /*json格式还是csrtuct格式*/
    uint32_t frameType;     /*NV12 or NV21*/
    uint32_t res[4];
}YUV_FRAME_INFO_HEAD;

/*obj rect coordinate*/
/*Len16*/
typedef struct _YUV_FRAME_RECT
{
    float x;
    float y;
    float w;
    float h;
}YUV_FRAME_RECT;

/*point coordinate Len8*/
typedef struct _YUV_FRAME_POINT_
{
    float x;
    float y;
}YUV_FRAME_POINT;

/*一个多边形规则*/
/*Len 8 +10*8=88*/
typedef struct _YUV_FRAME_RULE_INFO_
{
    uint64_t uPointNum;
    YUV_FRAME_POINT stPointList[YUV_FRAME_MAX_POINT_NUM];
}YUV_FRAME_RULE_INFO;

/*用户自定义属性 Len 16*/
typedef struct _YUV_FRAME_ATTR_INFO_
{
    /*标签描述字 精简,最大8字节*/
    char desc[YUV_FRAME_MAX_LABEL_DESC];
    /*标签,如男女,青壮年,眼镜*/
    uint32_t label;
    /*confindence==0表示无属性*/
    float confindence;
}YUV_FRAME_ATTR_INFO;
/*属性结构体 Len 8+8*16=136 */
typedef struct _YUV_FRAME_ATTR_LIST_
{
    uint64_t uAttrNum;
    YUV_FRAME_ATTR_INFO stAttrList[YUV_FRAME_MAX_ATTR_NUM];
}YUV_FRAME_ATTR_LIST;

/*单个obj对应所有属性 Len 4+4+16+16+136+80=256 */
typedef struct _YUV_FRAME_OBJ_INFO_
{
    float fConfindence;     /*置信度*/
    float fScore;           /*评分*/
    uint32_t uId;
    uint32_t reserve[3];
    YUV_FRAME_RECT stObjRect;    /*目标坐标*/
    YUV_FRAME_ATTR_LIST stAttr;
    char res[80];
}YUV_FRAME_OBJ_INFO;

/*32个objlist*/
/*Len 8+256*32=8200*/
typedef struct _YUV_FRAME_OBJ_LIST_
{
    uint64_t uObjNum;                           /*总共含有的目标数*/
    YUV_FRAME_OBJ_INFO stObjInfoList[YUV_FRAME_MAX_OBJ_NUM];    /*目标list*/
}YUV_FRAME_OBJ_LIST;

/* 4*4+8200+88=8304 */
typedef struct _YUV_FRAME_INFO_
{
    uint32_t w;
    uint32_t h;
    uint32_t stride;
    uint32_t res[1];
    YUV_FRAME_OBJ_LIST stObj;
    YUV_FRAME_RULE_INFO stRule;
}YUV_FRAME_DATA;

