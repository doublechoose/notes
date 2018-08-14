package com.nd.module_collections.ui.widget.dict;

import android.content.Context;
import android.content.res.TypedArray;
import android.graphics.Canvas;
import android.graphics.Color;
import android.graphics.Paint;
import android.graphics.Rect;
import android.graphics.drawable.Drawable;
import android.support.v7.widget.LinearLayoutManager;
import android.support.v7.widget.RecyclerView;
import android.util.TypedValue;
import android.view.View;

import com.nd.module_collections.sdk.bean.Favorite;
import com.nd.module_collections.ui.adapter.CollectionsDictAdapter;
import com.nd.smartcan.commons.util.helper.DateUtil;

import java.util.ArrayList;
import java.util.List;

/**
 * Created by WangZeshuang on 2017/4/26.
 */

public class TitleItemDecoration extends RecyclerView.ItemDecoration {

    private List<Favorite> mDatas = new ArrayList<>();
    private Paint mPaint;
    private Rect mBounds;//用于存放测量文字Rect

    private int mTitleHeight;//title的高
    private int mTitleLineHeight;//title的高
    private int mTitleMarginLeft;//title 的左边距
    private static int COLOR_TITLE_BG = Color.parseColor("#FFF5F5F5");
    private static int COLOR_TITLE_FONT = Color.parseColor("#FF999999");
    private static int COLOR_TITLE_LINE = Color.parseColor("#FFD9D9D9");
    //    private static int COLOR_TITLE_LINE = Color.parseColor("#FFFF0000");
    private static int mTitleFontSize;//title字体大小

    private int sortType;

    protected Drawable mDivider;
    private static final int[] ATTRS = new int[]{
            android.R.attr.listDivider
    };


    public TitleItemDecoration(Context context, List<Favorite> datas, int sortType) {
        super();
        mDatas = datas;
        if (datas!=null){
            mDatas.addAll(datas);
        }
        mPaint = new Paint();
        mBounds = new Rect();
        mTitleHeight = (int) TypedValue.applyDimension(TypedValue.COMPLEX_UNIT_DIP, 25, context.getResources().getDisplayMetrics());
        mTitleLineHeight = (int) TypedValue.applyDimension(TypedValue.COMPLEX_UNIT_DIP, 0.5f, context.getResources().getDisplayMetrics());
        mTitleMarginLeft = (int) TypedValue.applyDimension(TypedValue.COMPLEX_UNIT_DIP, 15, context.getResources().getDisplayMetrics());
        mTitleFontSize = (int) TypedValue.applyDimension(TypedValue.COMPLEX_UNIT_SP, 13, context.getResources().getDisplayMetrics());
        mPaint.setTextSize(mTitleFontSize);
        mPaint.setAntiAlias(true);

        final TypedArray a = context.obtainStyledAttributes(ATTRS);
        mDivider = a.getDrawable(0);
        a.recycle();

        this.sortType = sortType;
    }
    public TitleItemDecoration(Context context, int sortType) {
        super();
        mPaint = new Paint();
        mBounds = new Rect();
        mTitleHeight = (int) TypedValue.applyDimension(TypedValue.COMPLEX_UNIT_DIP, 25, context.getResources().getDisplayMetrics());
        mTitleLineHeight = (int) TypedValue.applyDimension(TypedValue.COMPLEX_UNIT_DIP, 0.5f, context.getResources().getDisplayMetrics());
        mTitleMarginLeft = (int) TypedValue.applyDimension(TypedValue.COMPLEX_UNIT_DIP, 15, context.getResources().getDisplayMetrics());
        mTitleFontSize = (int) TypedValue.applyDimension(TypedValue.COMPLEX_UNIT_SP, 13, context.getResources().getDisplayMetrics());
        mPaint.setTextSize(mTitleFontSize);
        mPaint.setAntiAlias(true);

        final TypedArray a = context.obtainStyledAttributes(ATTRS);
        mDivider = a.getDrawable(0);
        a.recycle();

        this.sortType = sortType;
    }

    @Override
    public void onDraw(Canvas c, RecyclerView parent, RecyclerView.State state) {
        super.onDraw(c, parent, state);
        final int left = parent.getLeft();
        final int right = parent.getWidth();
        final int childCount = parent.getChildCount();
        for (int i = 0; i < childCount; i++) {
            final View child = parent.getChildAt(i);
            final RecyclerView.LayoutParams params = (RecyclerView.LayoutParams) child
                    .getLayoutParams();
            int position = params.getViewLayoutPosition();
            //我记得Rv的item position在重置时可能为-1.保险点判断一下吧
            if (position > -1) {
                String tag = getTag(position);
                if (position == 0) {//等于0肯定要有title的
                    drawTitleArea(c, left, right, child, params, position);

                } else {//其他的通过判断
                    if (null != tag && !tag.equals(getTag(position - 1))) {
                        //不为空 且跟前一个tag不一样了，说明是新的分类，也要title
                        drawTitleArea(c, left, right, child, params, position);
                    }

                }

            }
        }
    }

    private void drawLine(Canvas c, int startX,int startY,int endX,int endY) {
        mPaint.setColor(COLOR_TITLE_LINE);
        c.drawLine(startX, startY, endX, endY, mPaint);
    }

    /**
     * 绘制Title区域背景和文字的方法
     */
    private void drawTitleArea(Canvas c, int left, int right, View child, RecyclerView.LayoutParams params, int position) {//最先调用，绘制在最下层


        /*画title区域背景*/
        mPaint.setColor(COLOR_TITLE_BG);
        c.drawRect(left, child.getTop() - params.topMargin - mTitleHeight, right, child.getTop() - params.topMargin, mPaint);

        /*画上面那条线*/
        drawLine(c,left, child.getTop() - params.topMargin - mTitleHeight, right, child.getTop() - params.topMargin - mTitleHeight);
        /*画下面那条线*/
        drawLine(c,left, child.getTop() - params.topMargin, right, child.getTop() - params.topMargin);
/*
        Paint.FontMetricsInt fontMetrics = mPaint.getFontMetricsInt();
        int baseline = (getMeasuredHeight() - fontMetrics.bottom + fontMetrics.top) / 2 - fontMetrics.top;*/
        mPaint.setColor(COLOR_TITLE_FONT);

        String tag = getTag(position);
        if (tag != null) {
            mPaint.getTextBounds(tag, 0, tag.length(), mBounds);
            c.drawText(tag, child.getPaddingLeft() + mTitleMarginLeft, child.getTop() - params.topMargin - (mTitleHeight / 2 - mBounds.height() / 2), mPaint);
        }
    }


    /*设置悬浮*/
    @Override
    public void onDrawOver(Canvas c, RecyclerView parent, RecyclerView.State state) {//最后调用 绘制在最上层
        int pos = ((LinearLayoutManager) (parent.getLayoutManager())).findFirstVisibleItemPosition();

        /*当一个item都没有的时候返回为-1*/
        if (pos<0){
            return;
        }
        String tag = getTag(pos);
        //View child = parent.getChildAt(pos);
        View child = parent.findViewHolderForLayoutPosition(pos).itemView;//出现一个奇怪的bug，有时候child为空，所以将 child = parent.getChildAt(i)。-》 parent.findViewHolderForLayoutPosition(pos).itemView
        mPaint.setColor(COLOR_TITLE_BG);
        c.drawRect(parent.getPaddingLeft(), parent.getPaddingTop(), parent.getRight() - parent.getPaddingRight(), parent.getPaddingTop() + mTitleHeight, mPaint);
        mPaint.setColor(COLOR_TITLE_FONT);
        if (tag != null) {

            mPaint.getTextBounds(tag, 0, tag.length(), mBounds);

            c.drawText(tag, child.getPaddingLeft() + mTitleMarginLeft,
                    parent.getPaddingTop() + mTitleHeight - (mTitleHeight / 2 - mBounds.height() / 2),
                    mPaint);
            drawLine(c,parent.getPaddingLeft(),parent.getPaddingTop() + mTitleHeight,parent.getRight() - parent.getPaddingRight(),parent.getPaddingTop() + mTitleHeight);
        }
    }

    @Override
    public void getItemOffsets(Rect outRect, View view, RecyclerView parent, RecyclerView.State state) {
        super.getItemOffsets(outRect, view, parent, state);
        int position = ((RecyclerView.LayoutParams) view.getLayoutParams()).getViewLayoutPosition();
        //我记得Rv的item position在重置时可能为-1.保险点判断一下吧
        if (position > -1) {
            if (position == 0) {//等于0肯定要有title的
                outRect.set(0, mTitleHeight, 0, 0);
            } else {//其他的通过判断
                String tag = getTag(position);
                String prevTag = getTag(position - 1);
                if (null != tag && !tag.equals(prevTag)) {
                    outRect.set(0, mTitleHeight, 0, 0);//不为空 且跟前一个tag不一样了，说明是新的分类，也要title
                } else {
                    outRect.set(0, 0, 0, 0);
                }
            }
        }
    }

    private String getTag(int position) {
        if (position > -1 && position < mDatas.size()) {
            if (sortType == CollectionsDictAdapter.PINYIN_SORT){
                if (mDatas.get(position).score!=null){
                    return mDatas.get(position).score.toUpperCase();
                }
            }else if (sortType == CollectionsDictAdapter.TIME_SORT){
                return DateUtil.getStringToDateStr(mDatas.get(position).create_time, DateUtil.NOW_DATE);
            }
        }
        return null;
    }
    public void setSortType(int sortType){
        this.sortType = sortType;
    }
    public void setList(List<Favorite> list){
        if (list !=null){
            mDatas = list;
        }
    }
}
