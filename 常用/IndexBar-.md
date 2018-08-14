/**
 * Created by WangZeshuang on 2017/4/20.
 */

public class IndexBar extends View implements View.OnTouchListener {
    private static final String[] INDEXES = new String[]{"#", "A", "B", "C", "D", "E", "F", "G", "H",
            "I", "J", "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z"};
    private static final int TOUCHED_BACKGROUND_COLOR = 0x40000000;
    private OnIndexChangedListener mListener;

    private List<String> mIndexDatas;
    private float indexTextSize;
    private int indexTextColor;

    /*view 宽高*/
    private int mWidth, mHeight;
    /*每个index区域的高度*/
    private int mGapHeight;
    /*index之间的距离*/
    private float mInterval;

    private Paint mPaint;

    private Rect mIndexBounds;

    public void setOnIndexChangedListener(OnIndexChangedListener listener) {
        mListener = listener;
    }

    public IndexBar(Context context) {
        this(context, null);
    }

    public IndexBar(Context context, AttributeSet attrs) {
        this(context, attrs, 0);
    }

    public IndexBar(Context context, AttributeSet attrs, int defStyleAttr) {
        super(context, attrs, defStyleAttr);
        init(attrs);
    }

    private void init(AttributeSet attrs) {
        TypedArray ta = getContext().obtainStyledAttributes(attrs, R.styleable.IndexBar);
        indexTextSize = ta.getDimension(R.styleable.IndexBar_indexTextSize, AndroidUtils.dip2px(getContext(), 16));
        mInterval = ta.getDimension(R.styleable.IndexBar_indexInterval, AndroidUtils.dip2px(getContext(), 16));
        indexTextColor = ta.getColor(R.styleable.IndexBar_indexTextColor, 0xFF96B0B0);
        ta.recycle();

        mIndexDatas = new ArrayList<>();
        setOnTouchListener(this);

        mPaint = new Paint();
        mPaint.setAntiAlias(true);
        mPaint.setTextSize(indexTextSize);
        mPaint.setColor(indexTextColor);
        mIndexBounds = new Rect();

    }

    @Override
    protected void onSizeChanged(int w, int h, int oldw, int oldh) {
        super.onSizeChanged(w, h, oldw, oldh);
        mWidth = w;
        mHeight =h;

        if (null == mIndexDatas || mIndexDatas.isEmpty()){
            return;
        }
        computeGapHeight();
    }

    @Override
    protected void onMeasure(int widthMeasureSpec, int heightMeasureSpec) {
        /*取出宽高的spec mode 和size*/
        int wMode = MeasureSpec.getMode(widthMeasureSpec);
        int wSize = MeasureSpec.getSize(widthMeasureSpec);
        int hMode = MeasureSpec.getMode(heightMeasureSpec);
        int hSize = MeasureSpec.getSize(heightMeasureSpec);

        int measureWidth = 0, measureHeight = 0;


        for (String index : mIndexDatas) {
            mPaint.getTextBounds(index,0,index.length(),mIndexBounds);//测量计算文字所在矩形，可以得到宽高
            mIndexBounds.set(mIndexBounds.left,mIndexBounds.top,mIndexBounds.right, (int) (mIndexBounds.bottom+mInterval));
            measureHeight = Math.max(mIndexBounds.height(),measureHeight);//循环结束后，得到index的最大高度
            measureWidth = Math.max(mIndexBounds.width(),measureWidth);//循环结束后，得到index的最大宽度
        }
        measureHeight *= mIndexDatas.size();
        switch (wMode){
            case MeasureSpec.EXACTLY:
                measureWidth = wSize;
                break;
            case MeasureSpec.AT_MOST:
                measureWidth = Math.min(measureWidth,wSize);
                break;

            case MeasureSpec.UNSPECIFIED:
                break;
        }
        switch (hMode){
            case MeasureSpec.EXACTLY:
                measureHeight = hSize;
                break;
            case MeasureSpec.AT_MOST:
                measureHeight = Math.min(measureHeight,hSize);
                break;

            case MeasureSpec.UNSPECIFIED:
                break;
        }

        setMeasuredDimension(measureWidth,measureHeight);
    }

    private void computeGapHeight() {
        if (mIndexDatas.size()>0){
            mGapHeight = (mHeight - getPaddingTop() - getPaddingBottom()) / mIndexDatas.size();
        }
    }



    @Override
    protected void onDraw(Canvas canvas) {
        int t = getPaddingTop();
        String index;
        for (int i = 0; i < mIndexDatas.size(); i++) {
            index = mIndexDatas.get(i);
            Paint.FontMetrics fontMetrics = mPaint.getFontMetrics();
            int baseline = (int) ((mGapHeight - fontMetrics.bottom-fontMetrics.top)/2);
            canvas.drawText(index,mWidth/2 - mPaint.measureText(index)/2,t+mGapHeight*i+baseline,mPaint);

        }
    }


    public void setIndexData(List<Favorite> sourceData) {
        if (sourceData != null) {

            mIndexDatas.clear();
            String indexTag;
            for (Favorite c : sourceData) {
                indexTag = c.getScore().toUpperCase();
                if (!mIndexDatas.contains(indexTag)) {
                    mIndexDatas.add(indexTag);
                }
            }
            invalidate();
            computeGapHeight();
        }
    }


    @Override
    public boolean onTouch(View v, MotionEvent event) {
        switch (event.getAction()) {
            case MotionEvent.ACTION_DOWN:
//                setBackgroundColor(TOUCHED_BACKGROUND_COLOR);
                handle(v, event);
                return true;
            case MotionEvent.ACTION_MOVE:
                handle(v, event);
                return true;
            case MotionEvent.ACTION_UP:
                setBackgroundColor(Color.TRANSPARENT);
                handle(v, event);
                return true;
        }
        return super.onTouchEvent(event);
    }

    private void handle(View v, MotionEvent event) {
        int y = (int) event.getY();
        int height = v.getHeight();
        int position = mIndexDatas.size() * y / height;
        if (position < 0) {
            position = 0;
        } else if (position >= mIndexDatas.size()) {
            position = mIndexDatas.size() - 1;
        }

        String index = mIndexDatas.get(position);
        boolean showIndicator = event.getAction() != MotionEvent.ACTION_UP;
        if (mListener != null) {
            mListener.onIndexChanged(index, showIndicator);
        }

    }


    public interface OnIndexChangedListener {
        void onIndexChanged(String index, boolean showIndicator);
    }
}
