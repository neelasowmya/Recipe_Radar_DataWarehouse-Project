-- 1. Write a sql query to analyze which recipe categories (like desserts, vegan, etc.) are most popular (top 10).
SELECT 
    RecipeCategory,
    COUNT(*) AS RecipeCount,
    AVG(AggregatedRating) AS AverageRating,
    SUM(ReviewCount) AS TotalReviews
FROM 
    archiveRecipe.Recipes
GROUP BY 
    RecipeCategory
ORDER BY 
    RecipeCount DESC, AverageRating DESC LIMIT 10;
-- 2. Write a query to assess the average nutritional values (like carbohydrates, protein) across different recipe categories
SELECT 
    RecipeCategory,
    AVG(CarbohydrateContent) AS AverageCarbohydrates,
    AVG(ProteinContent) AS AverageProtein
FROM 
    archiveRecipe.Recipes
GROUP BY 
    RecipeCategory LIMIT 10;
-- 3. Write a sql query to Identify top 10 authors who have contributed the most recipes.
SELECT 
    AuthorId,
    AuthorName,
    COUNT(*) AS NumberOfRecipes
FROM 
    archiveRecipe.Recipes
GROUP BY 
    AuthorId, AuthorName
ORDER BY 
    NumberOfRecipes DESC
LIMIT 10;
-- 4. Write a sql query to Determine the average preparation and cooking times across various types of recipes.
SELECT RecipeCategory, AVG(PrepTimeInMinutes) AS AveragePrepTime, AVG(CookTimeInMinutes) AS AverageCookTime FROM  archiveRecipe.Recipes WHERE 
PrepTimeInMinutes IS NOT NULL AND CookTimeInMinutes IS NOT NULL GROUP BY RecipeCategory LIMIT 25;
-- 5. Write a sql query to display the nutritional content of 10 highest popular recipes
SELECT Name, AggregatedRating, CarbohydrateContent,ProteinContent,FiberContent,FatContent FROM 
archiveRecipe.Recipes ORDER BY AggregatedRating DESC LIMIT 10;
-- 6. Write a sql query to display the nutritional content of 10 lowest rated recipes
SELECT Name, AggregatedRating, CarbohydrateContent,ProteinContent,FiberContent,FatContent FROM 
archiveRecipe.Recipes WHERE AggregatedRating IS NOT NULL ORDER BY AggregatedRating ASC LIMIT 10;
-- 7.Write a sql query to determine  how different factors like cooking time influence user ratings.
SELECT Name,AVG(AggregatedRating) AS AverageRating, AVG(ReviewCount) AS AverageReviewCount,AVG(CookTimeInMinutes) AS AverageCookTime,AVG(PrepTimeInMinutes) AS AveragePrepTime,FROM archiveRecipe.Recipes
GROUP BY Name ORDER BY AverageRating DESC, AverageReviewCount DESC LIMIT 10;
-- 8.Write a SQL Query to find recipes with low calorie count
SELECT 
    Name,
    CalorieContent
FROM 
    Recipes
WHERE 
    CalorieContent < 300
ORDER BY 
    CalorieContent;
-- 9.Write a sql query to fetch recipes with low fat content
SELECT Name,FatContent FROM archiveRecipe.Recipes WHERE FatContent < 10 AND FatContent != 0 ORDER BY FatContent LIMIT 20;
